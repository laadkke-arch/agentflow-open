require "/app/spec/rails_helper"
require_relative "harness"

RSpec.describe "AF-RES-241 Apply", type: :system, with_cache: true do
  include CandidateHelper
  include CourseOptionHelpers
  include Af241Harness

  def apply_fixture(group)
    @current_candidate = create(:candidate, email_address: "candidate-af241@example.test")
    given_i_am_signed_in_with_one_login
    case group
    when "A1"
      @current_candidate.application_forms.destroy_all
      @form = create(:completed_application_form, candidate: @current_candidate,
                    first_name: "Fixture", last_name: "Candidate", references_count: 0,
                    submitted_at: Time.zone.now, support_reference: "R241", recruitment_cycle_year: current_year)
      @reference = create(:reference, :not_requested_yet, application_form: @form,
                          name: "Morgan Example", referee_type: :academic,
                          email_address: "ref-one@example.test", relationship: "Synthetic academic supervisor")
      @second_reference = create(:reference, :not_requested_yet, application_form: @form,
                                 name: "Taylor Example", referee_type: :professional,
                                 email_address: "ref-two@example.test", relationship: "Synthetic colleague")
      @choice = create(:application_choice, :offered, application_form: @form)
      candidate_interface_accept_offer_path(@choice)
    when "A2"
      @form = @current_candidate.current_application || create(:application_form, candidate: @current_candidate)
      provider = create(:provider, name: "AF241 Training Provider", code: "R24", selectable_school: true)
      @course = create(:course, :open, :with_both_study_modes, name: "AF241 Mathematics", code: "T241", provider:)
      @other_course = create(:course, :open, name: "AF241 English", code: "T242", provider:, study_mode: :full_time)
      original_site = create(:site, provider:, name: "AF241 Original Site")
      additional_site = create(:site, provider:, name: "AF241 Additional Site")
      full_time = course_option_for_provider(provider:, course: @course, site: original_site, study_mode: "full_time")
      @same_site_part_time = course_option_for_provider(provider:, course: @course, site: original_site, study_mode: "part_time")
      course_option_for_provider(provider:, course: @course, site: additional_site, study_mode: "full_time")
      course_option_for_provider(provider:, course: @course, site: additional_site, study_mode: "part_time")
      course_option_for_provider(provider:, course: @other_course, site: original_site, study_mode: "full_time")
      @choice = create(:application_choice, :unsubmitted, application_form: @form,
                       course_option: full_time, personal_statement: "AF241 synthetic unchanged statement")
      candidate_interface_course_choices_course_review_path(@choice.id)
    when "A3"
      @form = @current_candidate.current_application || create(:application_form, candidate: @current_candidate)
      @form.update!(
        first_name: "Fixture", last_name: "Candidate", phone_number: "07700 900241",
        address_type: :uk, address_line1: "24 Example Street", address_line2: "Test building",
        address_line3: "London", address_line4: nil, postcode: "SW1A 1AA", country: "GB",
        first_nationality: "British", country_residency_since_birth: true, contact_details_completed: true,
      )
      candidate_interface_contact_information_review_path
    end
  end

  def apply_models(stage)
    records = { application_form: @form }
    if @choice
      choice = @choice.reload
      records[:application_choice] = choice
      records[:current_course] = {
        id: choice.current_course.id, name_and_code: choice.current_course.name_and_code,
        option_id: choice.current_course_option.id, site_id: choice.current_course_option.site_id,
        site_name: choice.current_course_option.site_name, study_mode: choice.current_course_option.study_mode,
      }
    end
    if @reference
      records[:reference] = @reference
      records[:second_reference] = @second_reference
    end
    if @course
      key = :"candidate_interface_course_selection_wizard_#{@form.id}_#{@choice.id}"
      records[:wizard_cache] = Rails.cache.read(key)
    end
    record_model(stage, records)
  end

  def apply_save(anchor, invalid:)
    case anchor
    when "A1-1"
      set_field("referee_type", "professional")
    when "A1-2"
      set_field("name", "Morgan Edited")
    when "A2-1"
      set_field("course_id", @other_course.id)
    when "A2-2"
      set_field("study_mode", "part_time")
    when "A3-1"
      set_field("phone_number", invalid ? "not a phone" : "07700 900242")
    when "A3-2"
      submit("address_fields")
      apply_models("after_address_type")
      set_field("address_line1", "25 Example Street")
    end
    result = submit("after_submit")
    if anchor == "A2-2" && result["inputs"].any? { |input| input["name"]&.end_with?("[course_option_id]") }
      apply_models("after_study_mode")
      set_field("course_option_id", @same_site_part_time.id, changed: false)
      submit("after_site")
    end
    if anchor == "A3-2" && result["inputs"].any? { |input| input["name"]&.end_with?("[since_birth]") }
      apply_models("after_address_fields")
      submit("after_existing_residency")
    end
    snapshot(invalid ? "validation" : "return")
  end

  anchors = {
    "A1-1" => ["reference type for Morgan Example", "referee_type"],
    "A1-2" => ["name for Morgan Example", "name"],
    "A2-1" => ["course for", "course_id"],
    "A2-2" => ["full time or part time for", "study_mode"],
    "A3-1" => ["phone number", "phone_number"],
    "A3-2" => ["address", "address_type"],
  }

  cases = anchors.keys.flat_map { |anchor| %w[S B].map { |branch| "#{anchor}-#{branch}" } }
  cases += %w[A3-1-POS A3-1-ERR]
  only = Regexp.new(ENV.fetch("AF241_ONLY", "-[SB]$"))
  cases.grep(only).each do |id|
    anchor = id.sub(/-(S|B|POS|ERR)$/, "")
    branch = id.split("-").last
    it id do
      suffix, first_field = anchors.fetch(anchor)
      capture(id, first_field:) do
        origin = apply_fixture(anchor[0, 2])
        suffix = "#{suffix} #{@course.name_and_code}" if @course
        @trace[:originPath] = origin
        @trace[:resource] = {
          application_form: @form.id, choice: @choice&.id, reference: @reference&.id, locale: I18n.locale,
          app_time: Time.zone.now.iso8601, role: "candidate",
        }
        apply_models("before")
        data = run_target(origin, suffix)
        apply_models("first_edit")
        expect(data["inputs"].any? { |input| input["name"]&.end_with?("[#{first_field}]") && input["visible"] }).to be(true)
        if branch == "B"
          return_without_saving
        else
          apply_save(anchor, invalid: branch == "ERR")
        end
        apply_models("after")
        if branch == "ERR"
          expect(@trace[:stages]["validation"]["errors"]).not_to be_empty
          expect(@form.reload.phone_number).to eq("07700 900241")
        end
      end
    end
  end
end
