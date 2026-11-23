#include <iostream>
#include <string>
#include <nlohmann/json-schema.hpp>

// Research-authored minimal diagnostic. It deliberately implements C2 only;
// accepting a bad pii is evidence against treating this schema as a full answer,
// not proof that no application using the library could implement C1.
int main() {
  using nlohmann::json;
  using nlohmann::json_schema::json_validator;
  json schema = json::parse(R"({
    "$schema":"http://json-schema.org/draft-07/schema#",
    "type":"object", "required":["columns","pii"],
    "properties":{
      "columns":{"type":"object","additionalProperties":{
        "type":"object","required":["column_datatype"],
        "properties":{"column_datatype":{"enum":["integer","string","object"]}}
      }},
      "pii":{"type":"array","items":{"type":"string"}}
    }
  })");
  json_validator validator;
  validator.set_root_schema(schema);
  json cases = json::parse(R"([
    {"id":"C2-positive", "input":{"columns":{"field1":{"column_datatype":"string"}},"pii":["field1"]}, "expected_validator_accept":true, "desired_full_contract_accept":true},
    {"id":"C2-negative", "input":{"columns":{"field1":{"column_datatype":"array"}},"pii":["field1"]}, "expected_validator_accept":false, "desired_full_contract_accept":false},
    {"id":"C1-near-negative", "input":{"columns":{"field1":{"column_datatype":"string"}},"pii":["missing_column"]}, "expected_validator_accept":true, "desired_full_contract_accept":false}
  ])");
  bool ok=true;
  for (auto &c : cases) {
    bool accepted=true;
    std::string diagnostic;
    try { validator.validate(c["input"]); }
    catch (const std::exception &e) { accepted=false; diagnostic=e.what(); }
    c["actual_validator_accept"]=accepted;
    c["diagnostic"]=diagnostic;
    ok = ok && (accepted == c["expected_validator_accept"].get<bool>());
  }
  std::cout << cases.dump(2) << '\n';
  return ok?0:1;
}
