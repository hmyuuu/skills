# Flowchart

Generate flowcharts using typst with cetz.

## User Request
$ARGUMENTS

## Input
```
start -> process A -> decision?
  yes -> B -> end
  no -> C -> A
```

## Output
```typst
#import "@preview/cetz:0.3.2"
#cetz.canvas({
  import cetz.draw: *
  // nodes and arrows
})
```
