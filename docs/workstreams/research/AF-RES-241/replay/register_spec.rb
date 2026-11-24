require "/app/spec/rails_helper"
require_relative "harness"

RSpec.describe "AF-RES-241 Register", type: :feature, js: true do
  include Af241Harness

  def register_fixture
    user = create(:user, email: "provider-af241@example.test", first_name: "Fixture", last_name: "Provider")
    given_i_am_authenticated(user: user)
    provider = current_user.organisation
    maths = SubjectSpecialism.find_by(name: CourseSubjects::MATHEMATICS) ||
      create(:subject_specialism, name: CourseSubjects::MATHEMATICS,
             allocation_subject: create(:allocation_subject, name: "Mathematics"))
    SubjectSpecialism.find_by(name: CourseSubjects::PRIMARY_TEACHING) ||
      create(:subject_specialism, name: CourseSubjects::PRIMARY_TEACHING,
             allocation_subject: create(:allocation_subject, name: "Primary teaching"))
    @trainee = create(
      :trainee, :draft, :with_apply_application, :provider_led_postgrad, provider: provider,
      apply_application: create(:apply_application, accredited_body_code: provider.code),
      first_names: "Fixture", middle_names: nil, last_name: "Trainee", email: "trainee-af241@example.test",
      sex: :sex_not_provided, nationalities: [create(:nationality, :british)],
      provider_trainee_id: "AF241-LOCAL", date_of_birth: Date.new(1991, 2, 24), course_education_phase: :secondary,
      course_subject_one: CourseSubjects::MATHEMATICS, course_subject_two: nil, course_subject_three: nil,
      course_allocation_subject: maths.allocation_subject, course_age_range: [11, 16], course_uuid: nil,
      training_initiative: :no_initiative, applying_for_bursary: false,
      applying_for_grant: false, applying_for_scholarship: false,
      study_mode: :full_time, itt_start_date: Date.new(2026, 9, 1), itt_end_date: Date.new(2027, 7, 31),
    )
    origin = trainee_check_details_path(@trainee)
    @trace[:originPath] = origin
    @trace[:resource] = {
      trainee_id: @trainee.id, trainee_slug: @trainee.slug, provider_id: provider.id,
      apply_application_id: @trainee.apply_application_id, locale: I18n.locale,
      app_time: Time.zone.now.iso8601, role: "provider"
    }
    visit trainee_review_drafts_path(@trainee)
    origin
  end

  def register_models(stage)
    trainee = @trainee.reload
    record_model(stage, {
      trainee: trainee, progress: trainee.progress,
      course_form_store: {
        training_routes: FormStore.get(trainee.id, :training_routes),
        course_education_phase: FormStore.get(trainee.id, :course_education_phase),
        course_details: FormStore.get(trainee.id, :course_details),
      },
    })
  end

  def complete_secondary_subject
    field = page.all("main input[role=combobox]").find { |item| item[:id].include?("course-subject-one") }
    if field
      field.set("Mathematics")
      page.find("[role=option]", exact_text: "Mathematics", match: :first).click
      @trace[:inputs_author_changed] << {
        name: field[:name], id: field[:id], value: "Mathematics", url: page.current_url, target_change: false,
      }
    else
      set_field("course_subject_one", CourseSubjects::MATHEMATICS, changed: false)
    end
  end

  def complete_required_course_fields(primary:)
    data = @trace[:stages].fetch("course_details")
    assert_field = ->(suffix) do
      data["inputs"].any? { |input| input["name"]&.end_with?("[#{suffix}]") && input["visible"] && !input["disabled"] }
    end
    if primary
      set_field("primary_course_subjects", PublishSubjects::PRIMARY_WITH_MATHEMATICS, changed: false)
      set_field("main_age_range", "5 to 11", changed: false)
    else
      complete_secondary_subject
      set_field("main_age_range", "11 to 16", changed: false)
    end
    if assert_field.call("study_mode") && data["inputs"].none? { |input| input["name"]&.end_with?("[study_mode]") && input["checked"] }
      set_field("study_mode", COURSE_STUDY_MODES[:full_time], changed: false)
    end
    dates = {
      "itt_start_date_3i" => "1", "itt_start_date_2i" => "9", "itt_start_date_1i" => "2026",
      "itt_end_date_3i" => "31", "itt_end_date_2i" => "7", "itt_end_date_1i" => "2027",
    }
    dates.each do |suffix, value|
      input = data["inputs"].find { |item| item["id"] == "course_details_form_#{suffix}" && item["visible"] }
      next unless input && input["value"].blank?

      # register_form_with can generate transient DOM names for these fields.
      page.find("[id=#{input.fetch('id').to_json}]").set(value)
      @trace[:inputs_author_changed] << {
        name: input["name"], id: input["id"], value: value, url: page.current_url, target_change: false,
      }
    end
  end

  def register_save(anchor)
    if anchor == "R1-1"
      set_field("training_route", TRAINING_ROUTE_ENUMS[:school_direct_salaried])
      submit("route_saved")
      register_models("after_route")
      set_field("course_education_phase", COURSE_EDUCATION_PHASE_ENUMS[:secondary], changed: false)
    else
      set_field("course_education_phase", COURSE_EDUCATION_PHASE_ENUMS[:primary])
    end
    submit("course_details")
    register_models("after_phase")
    complete_required_course_fields(primary: anchor == "R1-2")
    result = submit("return")
    register_models("after")
    expect(result["errors"]).to be_empty
    expect(URI(result["url"]).path).to eq(@trace[:originPath])
  end

  anchors = {
    "R1-1" => ["course", "training_route"],
    "R1-2" => ["education phase", "course_education_phase"],
  }
  only = Regexp.new(ENV.fetch("AF241_ONLY", "-[SB]$"))
  anchors.keys.flat_map { |anchor| %w[S B].map { |branch| "#{anchor}-#{branch}" } }.grep(only).each do |id|
    anchor = id[0, 4]
    it id do
      suffix, first_field = anchors.fetch(anchor)
      capture(id, first_field:) do
        origin = register_fixture
        register_models("before")
        data = run_target(origin, suffix)
        register_models("first_edit")
        expect(data["inputs"].any? { |input| input["name"]&.end_with?("[#{first_field}]") && input["visible"] }).to be(true)
        if id.end_with?("-B")
          return_without_saving
          register_models("after")
        else
          register_save(anchor)
        end
      end
    end
  end
end
