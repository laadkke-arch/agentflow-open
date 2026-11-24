require "json"
require "fileutils"
require "selenium-webdriver"

Capybara.server_host = "127.0.0.1"
Capybara.server_port = Integer(ENV.fetch("AF241_RAILS_PORT"))
Capybara.register_driver(:af241_chromium) do |app|
  options = Selenium::WebDriver::Chrome::Options.new(
    binary: "/usr/bin/chromium",
    args: %w[--headless --no-sandbox --disable-dev-shm-usage --disable-background-networking --window-size=1400,1000 --lang=en-GB],
  )
  Capybara::Selenium::Driver.new(
    app, browser: :remote, url: "http://127.0.0.1:14642", options: options,
  )
end

module Af241Harness
  DOM = <<~'JS'
    const main = document.querySelector("main") || document.body;
    const txt = (element) => element?.textContent?.replace(/\s+/g, " ").trim() ?? null;
    const attrs = (element) => Object.fromEntries(Array.from(element.attributes)
      .filter((a) => a.name.startsWith("aria-") || a.name === "role")
      .map((a) => [a.name, a.value]));
    const layout = (element) => {
      const style = getComputedStyle(element);
      return {
        display: style.display, visibility: style.visibility, clip: style.clip,
        width: style.width, height: style.height, position: style.position,
        overflow: style.overflow, backgroundColor: style.backgroundColor
      };
    };
    const links = Array.from(document.querySelectorAll("a"));
    const rowOf = (element) => element.closest(".govuk-summary-list__row, tr");
    function describeLink(a) {
      const hidden = Array.from(a.querySelectorAll(".govuk-visually-hidden,[hidden]"))
        .map((item) => ({ raw: item.textContent, attributes: attrs(item), layout: layout(item) }));
      const clone = a.cloneNode(true);
      clone.querySelectorAll(".govuk-visually-hidden,[hidden]").forEach((item) => item.remove());
      return {
        documentOrdinal: links.indexOf(a) + 1, rawText: a.textContent, innerText: a.innerText,
        visibleText: txt(clone), rawHref: a.getAttribute("href"), absoluteHref: a.href,
        attrs: attrs(a), hidden, outerHTML: a.outerHTML,
        rowKey: txt(rowOf(a)?.querySelector(".govuk-summary-list__key,th"))
      };
    }
    const visible = (element) => element.getClientRects().length > 0 &&
      !element.closest("[hidden],.govuk-radios__conditional--hidden") &&
      getComputedStyle(element).visibility !== "hidden";
    const buttons = Array.from(main.querySelectorAll("button,input[type=submit]")).filter(visible);
    const focus = document.activeElement;
    return {
      url: location.href, title: document.title, locale: document.documentElement.lang,
      bodyClass: document.body.className,
      h1: Array.from(main.querySelectorAll("h1")).map(txt),
      focused: {
        tag: focus?.tagName, id: focus?.id, name: focus?.getAttribute("name"),
        href: focus?.getAttribute("href"), role: focus?.getAttribute("role"),
        text: focus && !["BODY","HTML"].includes(focus.tagName) ? txt(focus)?.slice(0,200) : null
      },
      stylesheetCount: document.styleSheets.length,
      summaryLinks: Array.from(main.querySelectorAll("a[href]"))
        .filter((a) => rowOf(a) && a.textContent.trim().startsWith("Change"))
        .map(describeLink),
      backLinks: Array.from(document.querySelectorAll(".govuk-back-link, a")).filter(
        (a) => visible(a) && (a.classList.contains("govuk-back-link") || txt(a) === "Cancel")
      ).map(describeLink),
      summaryRows: Array.from(main.querySelectorAll(".govuk-summary-list__row")).map((row) => ({
        key: txt(row.querySelector(".govuk-summary-list__key")),
        value: txt(row.querySelector(".govuk-summary-list__value"))
      })),
      inputs: Array.from(main.querySelectorAll("input:not([type=hidden]):not([type=submit]),select,textarea")).map((input) => ({
        tag: input.tagName, type: input.type, name: input.name, id: input.id,
        value: input.value, checked: input.checked ?? null, disabled: input.disabled,
        readOnly: input.readOnly ?? null, visible: visible(input),
        labels: Array.from(input.labels || []).map(txt), attrs: attrs(input),
        options: input.tagName === "SELECT"
          ? Array.from(input.options).map((o) => ({value:o.value, text:txt(o), selected:o.selected}))
          : null,
        formAction: input.form?.getAttribute("action") || null,
        outerHTML: input.outerHTML
      })),
      submitButtons: buttons.map((button) => ({id:button.id, label:txt(button)||button.value, type:button.type})),
      errors: Array.from(main.querySelectorAll(".govuk-error-summary, .govuk-error-message")).map(txt)
    };
  JS

  def browser
    page.driver.browser
  end

  def initiate_capture(id, expected)
    @capture_id = id
    @trace = {
      id: id, expected: expected, browser: nil, stages: {},
      resource: {}, inputs_author_changed: [], models: {}, nav: [], errors: []
    }
    Capybara.current_driver = :af241_chromium
    I18n.locale = :en
    Faker::Config.random = Random.new(241)
    @trace[:browser] = {
      name: browser.capabilities.browser_name,
      version: browser.capabilities.browser_version,
      platform: browser.capabilities.platform_name,
      viewport: [1400, 1000],
    }
    persist
  end

  def persist
    dir = ENV.fetch("AF241_CAPTURE_DIR")
    FileUtils.mkdir_p(dir)
    File.write(File.join(dir, "#{@capture_id}.json"), JSON.pretty_generate(@trace.as_json) + "\n")
  end

  def cdp(command, **params)
    browser.execute_cdp(command, **params)
  end

  def snapshot(stage)
    page.has_css?("body", wait: 6)
    data = page.execute_script(DOM)
    @trace[:stages][stage] = data
    tree = cdp("Accessibility.getFullAXTree").fetch("nodes")
    preserve_roles = %w[link textField textFieldWithComboBox comboBox radio checkBox button heading alert]
    data["axNodesInTreeOrder"] = tree.each_with_index.filter_map do |node, ordinal|
      next unless !node["ignored"] && preserve_roles.include?(node.dig("role", "value"))

      { "treeOrdinal" => ordinal + 1, "cdpNode" => node }
    end
    data["summaryLinks"].each do |entry|
      ordinal = entry.fetch("documentOrdinal")
      # Resolve the live DOM node via its document order. This leaves the page DOM unchanged.
      object_id = cdp(
        "Runtime.evaluate",
        expression: "document.querySelectorAll('a')[#{ordinal - 1}]"
      ).dig("result", "objectId")
      next unless object_id

      backend_id = cdp("DOM.describeNode", objectId: object_id).dig("node", "backendNodeId")
      cdp("Runtime.releaseObject", objectId: object_id)
      entry["backendDOMNodeId"] = backend_id
      match = data["axNodesInTreeOrder"].find { |item| item.dig("cdpNode", "backendDOMNodeId") == backend_id }
      entry["ax"] = match
    end
    persist
    data
  end

  def activate_by_tab(entry)
    target_ordinal = entry.fetch("documentOrdinal")
    focus_ordinal = -1
    focused = []
    100.times do
      browser.action.send_keys(:tab).perform
      value = page.evaluate_script(<<~JS)
        (() => {
          const e = document.activeElement;
          return [Array.from(document.querySelectorAll("a")).indexOf(e)+1, e?.tagName,
            e?.id, e?.getAttribute("href"), e?.getAttribute("name")];
        })()
      JS
      focused << value
      focus_ordinal = value.first
      break if focus_ordinal == target_ordinal
    end
    @trace[:tabSteps] = focused
    @trace[:nav] << { method: "Tab/Enter", from: page.current_url, href: entry["absoluteHref"] }
    persist
    raise "Target link was not reached by Tab" unless focus_ordinal == target_ordinal

    before = page.current_url
    browser.action.send_keys(:enter).perform
    Selenium::WebDriver::Wait.new(timeout: 12).until { page.current_url != before }
    @trace[:nav].last[:landed] = page.current_url
  end

  def run_target(origin, suffix)
    visit origin
    data = snapshot("origin")
    matches = data["summaryLinks"].select do |entry|
      entry["hidden"].any? { |item| item["raw"].strip == suffix }
    end
    @trace[:selectedSuffix] = suffix
    @trace[:targetMatches] = matches.length
    persist
    raise "Expected one summary Change link for #{suffix.inspect}; found #{matches.length}" unless matches.one?

    activate_by_tab(matches.first)
    snapshot("first_edit")
  end

  def return_without_saving
    data = @trace[:stages].fetch("first_edit")
    back = data["backLinks"].first
    @trace[:nav] << {
      method: back ? "app back/cancel" : "browser Back",
      from: page.current_url, href: back&.fetch("rawHref"),
    }
    if back
      a = browser.find_elements(tag_name: "a").fetch(back.fetch("documentOrdinal") - 1)
      a.click
    else
      page.go_back
    end
    @trace[:nav].last[:landed] = page.current_url
    snapshot("return")
  end

  def set_field(suffix, value, changed: true)
    elements = page.all("main input:not([type=hidden]), main select, main textarea",
                        visible: :all, wait: 6).select do |element|
      element[:name]&.end_with?("[#{suffix}]")
    end
    element = elements.find do |item|
      !item.disabled? && (item[:type] == "radio" ? item[:value] == value.to_s : item.visible?)
    end
    raise "No editable #{suffix} accepts #{value.inspect}" unless element

    @trace[:inputs_author_changed] << {
      name: element[:name], id: element[:id], value: value, url: page.current_url, target_change: changed,
    }
    case element[:type]
    when "radio" then page.find("label[for=#{element[:id].to_json}]").click
    when "select-one"
      element.find("option[value=#{value.to_s.to_json}]", visible: :all).select_option
    else element.set(value.to_s)
    end
  end

  def submit(step)
    button = page.find("main button[type=submit], main input[type=submit]", match: :first, wait: 8)
    @trace[:nav] << { method: "form submit", from: page.current_url, label: button.text.presence || button[:value] }
    button.click
    # Selenium waits for native navigation. Wait for Turbo fetch/render if it remains on the same page.
    begin
      Selenium::WebDriver::Wait.new(timeout: 5).until do
        page.current_url != @trace[:nav].last[:from] || page.has_css?(".govuk-error-summary", wait: 0)
      end
    rescue Selenium::WebDriver::Error::TimeoutError
      # The snapshot records the actual unchanged URL and any visible errors.
    end
    @trace[:nav].last[:landed] = page.current_url
    snapshot(step)
  end

  def record_model(key, records)
    @trace[:models][key] = records.transform_values do |r|
      r.respond_to?(:reload) ? r.reload.attributes : r
    end
    persist
  end

  def capture(id, expected)
    initiate_capture(id, expected)
    yield
    @trace[:harness_completed] = true
  rescue StandardError => e
    if @trace
      @trace[:errors] << { class: e.class.name, message: e.message.lines.first.to_s.strip }
      begin
        snapshot("harness_error") if Capybara.current_driver == :af241_chromium
      rescue StandardError => capture_error
        @trace[:errors] << { class: capture_error.class.name, message: capture_error.message.lines.first.to_s.strip }
      end
    end
    raise
  ensure
    persist if @trace
  end
end
