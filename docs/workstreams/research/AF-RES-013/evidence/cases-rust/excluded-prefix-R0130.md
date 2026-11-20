# Design context

Decision cutoff (UTC date): 2014-07-30

Rust's borrow checker can treat the built-in owning pointer more precisely than other smart pointers that use user-defined dereferencing. It can recognize separate fields reached through the built-in pointer as distinct borrow paths, while invoking mutable dereferencing twice through another smart pointer may borrow the same receiver twice and fail. The goal is consistent treatment of the built-in pointer and user-defined smart pointers.

Find mechanisms or prior designs that resolve this discrepancy while preserving Rust's exclusive mutable-borrow rules. Consider what the compiler can establish about the dereferencing call and the resulting field accesses. Do not assume two arbitrary user-defined dereference operations are harmless merely because their final field names differ.
