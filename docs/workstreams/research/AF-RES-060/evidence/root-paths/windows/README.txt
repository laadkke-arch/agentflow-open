JSON schema validator for JSON for Modern C++


What is it?


This is a C++ library for validating JSON documents based on a
JSON Schema which itself should validate with
draft-7 of JSON Schema Validation.


First a disclaimer: It is work in progress and
contributions or hints or discussions are welcome.


Niels Lohmann et al develop a great JSON parser for C++ called JSON for Modern
C++. This validator is based on this
library, hence the name.


External documentation is missing as well. However the API of the validator
is rather simple.


New in version 2


Although significant changes have been done for the 2nd version
(a complete rewrite) the API is compatible with the 1.0.0 release. Except for
the namespace which is now nlohmann::json_schema.


Version 2 supports JSON schema draft 7, whereas 1 was supporting draft 4
only. Please update your schemas.


The primary change in 2 is the way a schema is used. While in version 1 the schema was
kept as a JSON-document and used again and again during validation, in version 2 the schema
is parsed into compiled C++ objects which are then used during validation. There are surely
still optimizations to be done, but validation speed has improved by factor 100
or more.


Design goals


The main goal of this validator is to produce human-comprehensible error
messages if a JSON-document/instance does not comply to its schema.


By default this is done with exceptions thrown at the users with a helpful
message telling what's wrong with the document while validating.


Starting with 2.0.0 the user can pass a json_schema::basic_error_handler-derived
object along with the instance to validate to receive a callback each time
a validation error occurs and decide what to do (throwing, counting, collecting).


Another goal was to use Niels Lohmann's JSON-library. This is why the validator
lives in his namespace.


Thread-safety


Instance validation is thread-safe and the same validator-object can be used by
different threads:


The validate method is const which indicates the object is not modified when
being called:


	json json_validator::validate(const json &) const;



Validator-object creation however is not thread-safe. A validator has to be
created in one (main?) thread once.


Weaknesses


Numerical validation uses nlohmann-json's integer, unsigned and floating point
types, depending on if the schema type is "integer" or "number". Bignum
(i.e. arbitrary precision and range) is not supported at this time.


Building


This library is based on Niels Lohmann's JSON-library and thus has
a build-dependency to it.


Currently at least version 3.8.0 of NLohmann's JSON library
is required.


Various methods using CMake can be used to build this project.


Build out-of-source


Do not run cmake inside the source-dir. Rather create a dedicated build-dir:


git clone https://github.com/pboettch/json-schema-validator.git
cd json-schema-validator
mkdir build
cd build
cmake [..]
make
make install # if needed
ctest # run unit, non-regression and test-suite tests



Building as shared library


By default a static library is built. A shared library is built with the option JSON_VALIDATOR_SHARED_LIBS,
whose default is the value of CMake's BUILD_SHARED_LIBS:


cmake [..] -DJSON_VALIDATOR_SHARED_LIBS=ON [..]



On
