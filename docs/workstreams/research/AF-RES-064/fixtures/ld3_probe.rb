# Execute LD-3 against the exact Ruby gem with explicit provenance arms.
require "json"
require "digest"
require "json/ld"

fixture = JSON.parse(File.read(File.join(__dir__, "ld3.json")))
context_dir = ARGV.fetch(0)
vc_url = fixture.fetch("document").fetch("@context").fetch(0)
bbs_url = fixture.fetch("document").fetch("@context").fetch(1)
author_url = fixture.fetch("document").fetch("@context").fetch(2)

def copy(object)
  Marshal.load(Marshal.dump(object))
end

def read_pinned_context(directory, name, expected)
  file = File.join(directory, name)
  raise "Wrong context digest for #{name}" unless Digest::SHA256.file(file).hexdigest == expected

  JSON.parse(File.read(file))
end

vc = read_pinned_context(context_dir, "vc-historical.json", "ab4ddd9a531758807a79a5b450510d61ae8d147eab966cc9a200c07095b0cdcc")
bbs = read_pinned_context(context_dir, "bbs-historical.json", "13c9ca884f29b002e9440d2a9b7aaf8611cf8f5b06fefb82161f9b81a67cebf2")
author_context = fixture.fetch("author_context")
arms = %w[literal_urls historical_alias reconstructed_nodes]
if ARGV[1] == "archived_singular"
  bbs = read_pinned_context(context_dir, "bbs-singular.json", "076dd3778a8969679612a092e4d3d52a1a7c12397b0a9b33ae69abeb75f02c22")
  arms = ["archived_singular"]
end

arms.each do |arm|
  fixture.fetch("groups").each do |group|
    document = copy(fixture.fetch("document"))
    document.fetch("credentialSubject")["values"] = copy(group.fetch("values"))
    document["expirationDate"] = group["expirationDate"] if group.key?("expirationDate")
    frame = copy(fixture.fetch("frame"))

    retrieved = {vc_url => vc, author_url => author_context}
    if %w[historical_alias archived_singular].include?(arm)
      retrieved[bbs_url] = bbs
    elsif arm == "reconstructed_nodes"
      context = copy(fixture.fetch("diagnostic_context"))
      document["@context"] = context
      frame = copy(fixture.fetch("diagnostic_frame"))
      frame["@context"] = copy(context)
    end
    loader_calls = []
    loader = lambda do |url, **_options, &block|
      loader_calls << url.to_s
      unless retrieved.key?(url.to_s)
        raise JSON::LD::JsonLdError::LoadingDocumentFailed,
          "Offline fixture has no verified deployment for #{url}"
      end

      block.call(JSON::LD::API::RemoteDocument.new(copy(retrieved.fetch(url.to_s)),
        documentUrl: url.to_s, contentType: "application/ld+json"))
    end
    expected_values = group.fetch("expected_values")
    before = copy(document)
    row = {
      arm: arm, group: group.fetch("id"), input: before, frame: copy(frame),
      expected_values: expected_values, expected_context_preserved: true,
      version: Gem.loaded_specs.fetch("json-ld").version.to_s, ruby: RUBY_DESCRIPTION
    }

    begin
      raw = JSON::LD::API.frame(document, frame, processingMode: "json-ld-1.1", compactArrays: true,
        omitGraph: true, ordered: true, documentLoader: loader)
      found_subject = raw.is_a?(Hash) ? raw["credentialSubject"] : nil
      values = found_subject.is_a?(Hash) ? found_subject["values"] : nil
      values_array = values.is_a?(Array) ? values : (values.nil? ? [] : [values])
      selected_values = values_array.map { |item| item.is_a?(Hash) ? item["a"] : nil }
      expected_keys = before.keys - ["@context", "credentialSubject"]
      subject_keys = before.fetch("credentialSubject").keys - ["values"]
      other_fields_ok = raw.is_a?(Hash) && expected_keys.all? { |key| before[key] == raw[key] } &&
        found_subject.is_a?(Hash) && subject_keys.all? { |key| before.fetch("credentialSubject")[key] == found_subject[key] }
      context_ok = raw.is_a?(Hash) && raw["@context"] == before["@context"]
      row.merge!(
        output: raw, selected_a_values: selected_values, found_b_c_and_shape: values_array == expected_values,
        C1: selected_values == expected_values.map { |value| value.fetch("a") },
        C2: values_array == expected_values && other_fields_ok && context_ok,
        other_credential_fields_exact: other_fields_ok, context_exact: context_ok,
        values_array_envelope: values.is_a?(Array) || (expected_values.empty? && values.nil?),
        case_status: "returned"
      )
    rescue StandardError => error
      row.merge!(C1: nil, C2: nil, case_status: "engine_error", error_type: error.class.name,
        error: error.message, backtrace: error.full_message(highlight: false))
    end
    row.merge!(input_after: document, unchanged: document == before, loader_calls: loader_calls)
    puts JSON.generate(row)
  end
end
