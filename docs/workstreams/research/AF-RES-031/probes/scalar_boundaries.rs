use std::sync::Arc;

use arrow::array::{ArrayRef, BinaryArray, BooleanArray, Int32Builder, ListBuilder, StringArray};
use arrow::datatypes::DataType;
use datafusion::{error::DataFusionError, scalar::ScalarValue};

fn observe(label: &str, array: &ArrayRef, index: usize, expected: ScalarValue) {
    let value = ScalarValue::try_from_array(array, index).expect("valid scalar access");
    println!("{} index={} value={:?}", label, index, value);
    assert_eq!(value, expected);
}

#[test]
fn supported_array_to_enum() {
    let boolean: ArrayRef = Arc::new(BooleanArray::from(vec![Some(true), None]));
    observe("Boolean", &boolean, 0, ScalarValue::Boolean(Some(true)));
    observe("Boolean", &boolean, 1, ScalarValue::Boolean(None));

    let utf8: ArrayRef = Arc::new(StringArray::from(vec![Some("alpha"), None]));
    observe("Utf8", &utf8, 0, ScalarValue::Utf8(Some("alpha".into())));
    observe("Utf8", &utf8, 1, ScalarValue::Utf8(None));

    let mut builder = ListBuilder::new(Int32Builder::new(4));
    builder.values().append_value(7).unwrap();
    builder.values().append_null().unwrap();
    builder.append(true).unwrap();
    builder.append(false).unwrap();
    let list: ArrayRef = Arc::new(builder.finish());
    observe(
        "List",
        &list,
        0,
        ScalarValue::List(
            Some(vec![ScalarValue::Int32(Some(7)), ScalarValue::Int32(None)]),
            DataType::Int32,
        ),
    );
    observe("List", &list, 1, ScalarValue::List(None, DataType::Int32));
}

#[test]
fn unsupported_binary_array_to_enum() {
    let binary: ArrayRef = Arc::new(BinaryArray::from(vec![Some(&b"unsupported"[..])]));
    let error = ScalarValue::try_from_array(&binary, 0).expect_err("Binary is unsupported");
    println!("Binary index=0 error={:?}", error);
    match error {
        DataFusionError::NotImplemented(text) => {
            assert_eq!(text, "Can't create a scalar of array of type \"Binary\"");
        }
        other => panic!("unexpected error: {:?}", other),
    }
}
