#set page(width: 300pt, height: 216pt, margin: 20pt)
#let my-fig(..args, placement: none) = {
  if placement == "p" { page[ #set align(center + horizon); #figure(..args) ] }
  else { figure(..args, placement: placement) }
}
BEFORE
#my-fig(rect(width: 100pt, height: 60pt, fill: aqua), caption: [CAP], placement: "p")
AFTER
