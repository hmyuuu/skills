---
name: flowchart
description: Generate flowcharts and diagrams using typst with cetz
---

# Flowchart (L2 - Directed)

You are executing the flowchart skill.

## User Request
$ARGUMENTS

## Purpose
Generate flowcharts, state diagrams, and process flows using typst and cetz.

## Autonomy Level: L2 (Directed)
- **Human**: Describe the flow, review output
- **AI**: Generate cetz code, compile, iterate

## Input
Describe your flowchart in plain text or structured format:
```
start -> process A -> decision?
  yes -> process B -> end
  no -> process C -> process A
```

## Output Template

```typst
#import "@preview/cetz:0.3.2"

#cetz.canvas({
  import cetz.draw: *
  
  // Styles
  let node(pos, label, name, shape: "rect") = {
    if shape == "rect" {
      rect(
        (pos.at(0) - 1, pos.at(1) - 0.4),
        (pos.at(0) + 1, pos.at(1) + 0.4),
        name: name
      )
    } else if shape == "diamond" {
      // Decision node
      let s = 0.6
      line(
        (pos.at(0), pos.at(1) + s),
        (pos.at(0) + s, pos.at(1)),
        (pos.at(0), pos.at(1) - s),
        (pos.at(0) - s, pos.at(1)),
        close: true,
        name: name
      )
    } else if shape == "circle" {
      circle(pos, radius: 0.4, name: name)
    }
    content(pos, label)
  }
  
  let arrow(from, to, label: none, anchor: "south") = {
    line(from, to, mark: (end: ">"))
    if label != none {
      content((from, 50%, to), label, anchor: anchor)
    }
  }
  
  // Nodes
  node((0, 4), "Start", "start", shape: "circle")
  node((0, 2), "Process A", "a")
  node((0, 0), "Decision?", "d", shape: "diamond")
  node((2, 0), "Process B", "b")
  node((-2, 0), "Process C", "c")
  node((2, -2), "End", "end", shape: "circle")
  
  // Arrows
  arrow("start.south", "a.north")
  arrow("a.south", "d.north")
  arrow("d.east", "b.west", label: "yes")
  arrow("d.west", "c.east", label: "no")
  arrow("b.south", "end.north")
  arrow("c.south", (rel: (0, -1)), (rel: (0, 0)), "a.west")
})
```

## Node Types

| Shape | Use | Cetz |
|-------|-----|------|
| Rectangle | Process/Action | `rect()` |
| Diamond | Decision | 4-point `line()` |
| Circle | Start/End | `circle()` |
| Parallelogram | Input/Output | skewed `line()` |

## Common Patterns

### Sequential
```
A -> B -> C -> D
```

### Branch
```
A -> B?
  yes -> C
  no -> D
```

### Loop
```
A -> B -> check?
  continue -> B
  done -> C
```

## Human Checkpoint
- Verify flow logic matches intent
- Check labels are clear
- Adjust layout/spacing as needed
