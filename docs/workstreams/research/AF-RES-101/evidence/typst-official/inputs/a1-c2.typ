#set page(height: 16.5cm, width: 18cm, margin: 1cm)
#set text(14pt, fill: rgb("#444444"))
#let members = range(1, 5).map(i => [Author #i \ Lab #i \ #link("mailto:author" + str(i) + "@example.invalid")])
#let edges = (paint: silver, thickness: 1pt, dash: "dashed")
#let framed(item) = {
  set align(center + horizon)
  box(width: 100%, height: 100%, stroke: edges, item)
}
#grid(columns: (1fr, 1fr), rows: (1fr, 1fr, 1fr, 1fr), row-gutter: 1cm, ..members.map(framed))
