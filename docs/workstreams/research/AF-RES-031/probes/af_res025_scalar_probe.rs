// Not executed in AF-RES-025. Copy into the fixed historical checkout's
// rust/datafusion/tests/ directory, not into the study's frozen result files.
use std::sync::Arc;
use arrow::array::{ArrayRef, BooleanArray, Int32Builder, ListBuilder, StringArray};
use arrow::datatypes::DataType;
use datafusion::scalar::ScalarValue;

#[test]
fn common_accessor_boolean_utf8_list() {
    let boolean: ArrayRef = Arc::new(BooleanArray::from(vec![Some(true), None]));
    assert_eq!(ScalarValue::try_from_array(&boolean, 0).unwrap(),
               ScalarValue::Boolean(Some(true)));
    assert_eq!(ScalarValue::try_from_array(&boolean, 1).unwrap(),
               ScalarValue::Boolean(None));
    let utf8: ArrayRef = Arc::new(StringArray::from(vec![Some("alpha"), None]));
    assert_eq!(ScalarValue::try_from_array(&utf8, 0).unwrap(),
               ScalarValue::Utf8(Some("alpha".to_owned())));
    assert_eq!(ScalarValue::try_from_array(&utf8, 1).unwrap(),
               ScalarValue::Utf8(None));
    let mut builder = ListBuilder::new(Int32Builder::new(4));
    builder.values().append_value(7).unwrap();
    builder.values().append_null().unwrap();
    builder.append(true).unwrap();
    builder.append(false).unwrap();
    let list: ArrayRef = Arc::new(builder.finish());
    assert_eq!(ScalarValue::try_from_array(&list, 0).unwrap(),
               ScalarValue::List(Some(vec![ScalarValue::Int32(Some(7)),
                                          ScalarValue::Int32(None)]), DataType::Int32));
    assert_eq!(ScalarValue::try_from_array(&list, 1).unwrap(),
               ScalarValue::List(None, DataType::Int32));
}
