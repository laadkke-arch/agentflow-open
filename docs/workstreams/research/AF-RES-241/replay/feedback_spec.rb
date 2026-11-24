require "/app/spec/rails_helper"
require_relative "harness"

RSpec.describe "AF-RES-241 Register feedback contrast", type: :feature, js: true do
  include Af241Harness

  {
    "C-R-F1" => "satisfaction level",
    "C-R-F2" => "improvement suggestion",
  }.each do |id, suffix|
    it id do
      capture(id, editable_group: "feedback form", link_purpose: suffix) do
        @trace[:resource] = { role: "anonymous local test session", locale: I18n.locale }
        visit new_feedback_path
        page.choose("Satisfied", allow_label_click: true)
        page.fill_in("How could we improve this service?", with: "Synthetic baseline suggestion")
        page.fill_in("Your name", with: "Fixture Feedback")
        page.fill_in("Your email address", with: "feedback-af241@example.test")
        submit("baseline_stashed")
        record_model("before", { feedback_item_count: FeedbackItem.count })
        data = run_target(feedback_check_path, suffix)
        expect(URI(data["url"]).path).to eq(new_feedback_path)
        if id == "C-R-F1"
          set_field("satisfaction_level", :very_dissatisfied)
        else
          field = page.find(:fillable_field, "How could we improve this service?")
          field.set("Synthetic edited suggestion")
          @trace[:inputs_author_changed] << {
            name: field[:name], id: field[:id], value: "Synthetic edited suggestion",
            url: page.current_url, target_change: true,
          }
        end
        result = submit("return")
        expect(URI(result["url"]).path).to eq(feedback_check_path)
        record_model("after", { feedback_item_count: FeedbackItem.count })
        expect(FeedbackItem.count).to eq(0)
      end
    end
  end
end
