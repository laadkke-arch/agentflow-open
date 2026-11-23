def bracketed:
  limit(1;
    foreach (explode[] | [.] | implode) as $c
      ({depth: 0, seen: false, text: ""};
       .text += $c
       | if $c == "[" then .depth += 1 | .seen = true
         elif $c == "]" then .depth -= 1
         else . end;
       if .seen and .depth == 0 then .text else empty end));
. as $s
| match("specificword=\\["; "g")
| .offset as $i
| $s[$i:]
| bracketed
