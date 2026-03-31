# Inline Visualization Skill — Design Spec

**Date:** 2026-03-31
**Status:** Draft
**Plugin:** `inline-viz` (in `hmyuuu-skills` marketplace)

## Summary

A Claude Code plugin that enables any CLI agent to render scientific diagrams and plots inline in the terminal via typst, and read back the output for iterative refinement. Three-layer architecture: terminal display, typst render engine, and domain-specific visualization templates.

## Goals

- Display typst-rendered SVG/PNG/PDF inline in iTerm2, Kitty, Ghostty, WezTerm
- Agent can read back rendered output (source for structure, vision for aesthetics)
- Support iterative refinement ("move figure 2 left" → re-render → verify)
- Support live MCP data visualization with adaptive updates
- Extensible: new viz types = new .typ templates, no core changes

## Non-Goals

- Web-based or browser agents (CLI agents with Bash access only)
- GUI annotation tools (text-first iteration; annotation extensible later)
- Replacing typst or CeTZ — this wraps them, doesn't reinvent them

---

## Architecture

### Three-Layer Stack

```
Agent / Skill
  │ writes .typ (from scratch or using template)
  ▼
Layer 3: Viz Libraries (optional)
  │ domain-specific .typ templates
  │ quantum-control.typ, qec.typ, tensor-network.typ, etc.
  │ output: .typ file ready to compile
  ▼
Layer 2: Render Engine (vizrender)
  │ typst compile → SVG (primary) + PNG (for display)
  │ calls vizshow for terminal display
  │ prints structured output: source path, SVG path, PNG path
  ▼
Layer 1: Terminal Display (vizshow)
  │ auto-detects terminal protocol
  │ emits inline image via escape sequences
  │ prints file path for agent readback
  ▼
Image displayed inline in terminal
```

### SVG as Primary Format

SVG is the default intermediate format throughout the pipeline:

- **typst → SVG** is native and fast
- **Agent readback**: SVG is XML — agent can grep/parse structure without vision tokens (e.g., "find all nodes with bond dimension > 8")
- **Terminal display**: SVG → PNG conversion at display time only (terminal protocols need raster)
- **Export**: SVG embeds directly in papers, web, slides
- **PDF**: typst outputs PDF directly when needed (e.g., `--format pdf`)

---

## Layer 1: `vizshow` — Terminal Display

**Location:** `${CLAUDE_PLUGIN_ROOT}/scripts/vizshow`
**Language:** Bash (~150 lines)
**Dependencies:** None required (native protocol emission via printf + base64)

### Interface

```
vizshow <image-file> [OPTIONS]

Options:
  --width N        Max width in terminal columns (default: auto from $COLUMNS)
  --height N       Max height in terminal rows (default: auto)
  --protocol P     Force protocol: iterm2|kitty|sixel|timg|chafa|file
  --fallback F     No protocol: save|ascii (default: save)
  --quiet          Suppress file path output
```

### Protocol Detection Order

1. `$TERM_PROGRAM == "iTerm.app"` → iTerm2 OSC 1337 (printf + base64)
2. `$KITTY_PID` set → Kitty graphics protocol (chunked PNG transfer)
3. `$GHOSTTY_RESOURCES_DIR` set → Kitty graphics protocol
4. `$WEZTERM_EXECUTABLE` set → iTerm2 OSC 1337
5. `command -v timg` → timg (auto-detects protocol)
6. `command -v chafa` → chafa (auto-detects protocol)
7. `command -v imgcat` → imgcat (iTerm2 bundled)
8. `command -v kitten` → kitten icat (Kitty bundled)
9. Fallback mode (save path or ASCII art)

### Output

```
<escape sequences rendering the image inline>

[vizshow: /absolute/path/to/file.png via iterm2]
```

### Exit Codes

- `0` — displayed inline successfully
- `1` — error (file not found, invalid format)
- `2` — fallback used (no inline protocol available)

### Design Constraints

- Accepts any image format (PNG, JPEG, GIF, PDF, SVG)
- No format conversion — that is Layer 2's job
- Always prints file path so agent can Read it back
- Auto-sizes to terminal width via `$COLUMNS` / `tput cols`
- Standalone: any skill or agent can use it for any image

---

## Layer 2: `vizrender` — Typst Render Engine

**Location:** `${CLAUDE_PLUGIN_ROOT}/scripts/vizrender`
**Language:** Bash (~100 lines)
**Dependencies:** `typst` CLI, one of: `rsvg-convert`, `magick`, or typst direct PNG output

### Interface

```
vizrender <input.typ> [OPTIONS]

Options:
  --format F       Output: svg|png|pdf (default: svg)
  --display        Display inline via vizshow (default: on)
  --no-display     Render only, don't display
  --output PATH    Custom output path (default: same dir as input, same basename)
  --width N        Pass --width to vizshow
  --open           Open in system viewer instead of terminal
```

### Pipeline

```
input.typ
  │
  ▼
typst compile input.typ output.svg
  │
  ├── SVG kept as primary artifact
  │
  ├── For terminal display: SVG → PNG conversion
  │   Priority: rsvg-convert → magick convert → typst compile --format png
  │
  ▼
vizshow output.png --width N
  │
  ▼
Structured output:
  [vizrender: input.typ → output.svg]
  [vizrender: source=/absolute/path/input.typ]
  [vizrender: rendered=/absolute/path/output.svg]
  [vizrender: displayed=/absolute/path/output.png]
```

### Readback Patterns

| Mode | How | Cost | Use When |
|------|-----|------|----------|
| Source readback | Read the .typ file | Cheap | Iterative refinement, parameter tweaking |
| SVG readback | Grep/parse the .svg XML | Cheap | Structural analysis (find nodes, edges, labels) |
| Vision readback | Read the .png via Read tool | Costly | Visual verification, layout judgment, aesthetics |

### Live Update Patterns

**Slow mode (30s+ intervals):**
Agent polls MCP → updates data → writes .typ → calls vizrender → displays. Simple loop, agent controls timing.

**Fast mode (1-5s intervals):**
Agent starts `vizrender input.typ --watch` in background (wraps `typst watch`). Agent updates .typ source only. Periodically calls `vizshow output.png` to re-display latest render.

### Typst Package Resolution

- Standard `@preview/` packages resolve via typst's native package system
- Viz library templates are local .typ files in the plugin. Since typst `#import` needs a literal path (not shell variables), `vizrender` resolves `${CLAUDE_PLUGIN_ROOT}` and passes it to typst via `--root` or the agent writes the absolute path directly. Alternatively, vizrender can inject a `--input template-dir=<path>` flag so the .typ file uses `#import sys.inputs.template-dir + "/qec.typ"`.
- Agent can also write standalone .typ without any template — most common for simple or custom diagrams

---

## Layer 3: Viz Library Templates

**Location:** `${CLAUDE_PLUGIN_ROOT}/templates/`

Templates are thin wrappers around underlying typst packages. They add convenience functions (overlays, multi-panel layouts, comparison modes). The agent can always write `.typ` from scratch without templates.

### Template Catalog

| File | Wraps | Priority | Key Functions |
|------|-------|----------|---------------|
| `pixel-art.typ` | `@preview/pixel-family` | 1st (smoke test) | `scene()` — compose characters with labels |
| `qec.typ` | `@preview/qec-thrust` + CeTZ | High | `qec-surface()`, `mark-errors()`, `show-matching()`, `highlight-logical()` |
| `quantum-control.typ` | CeTZ | High | `control-panel(circuit, trajectory, pulses, fidelity-sweep)` — 2x2 multi-panel |
| `tensor-network.typ` | CeTZ | Medium | `mps()`, `honeycomb()`, `mera()`, `ipeps()` — bond-labeled graph drawing |
| `bdd.typ` | `@preview/typdd` | Medium | `bdd-compare()` — side-by-side variable ordering comparison |
| `feynman.typ` | CeTZ | Medium | `feynman-diagram()` — propagator styles (wavy, curly, straight, dashed), vertex labels |
| `plot.typ` | CeTZ plot | Later | `line-plot()`, `scatter()`, `heatmap()`, `histogram()` — generic data viz |
| `paper-layout.typ` | Typst grid | Later | `figure-panel()` — multi-panel figure arrangement with labels (a, b, c, d) |

### Template Design Principles

- **Thin wrappers**: import the real package, add convenience functions
- **Data-driven**: accept structured data (arrays, dicts), not drawing commands
- **Auto-sizing**: `set page(width: auto, height: auto)` by default for inline display
- **Composable**: templates can be combined (e.g., quantum-control uses plot.typ internally)

---

## SKILL.md Structure

**Location:** `plugins/inline-viz/skills/inline-viz/SKILL.md`

```yaml
---
name: inline-viz
description: >
  Use when the user asks to visualize, plot, diagram, or render
  any scientific figure inline in the terminal. Supports quantum
  circuits, tensor networks, QEC codes, BDDs, Feynman diagrams,
  Bloch spheres, data plots, paper layouts, and pixel art.
---
```

### Sections

1. **Quick Start** — minimal pixel-family example showing full pipeline
2. **Core Workflow** — write .typ → vizrender → parse output → readback
3. **Available Templates** — table with import paths and when to use vs write from scratch
4. **Readback Patterns** — source vs SVG grep vs vision, decision guide
5. **Iteration Workflow** — user feedback → modify .typ → re-render → verify
6. **Live Update Pattern** — MCP polling → update → re-render → display (slow/fast modes)
7. **Display-Only** — vizshow for existing images (not typst-generated)
8. **Troubleshooting** — typst not installed, no terminal protocol, missing conversion tools

### Supporting File

`reference.md` alongside SKILL.md — quick-reference table of all template APIs, kept short for token efficiency.

---

## Plugin Structure

```
plugins/inline-viz/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── inline-viz/
│       ├── SKILL.md
│       └── reference.md
├── scripts/
│   ├── vizshow                  # Layer 1 (~150 LOC bash)
│   └── vizrender                # Layer 2 (~100 LOC bash)
└── templates/                   # Layer 3
    ├── pixel-art.typ
    ├── qec.typ
    ├── quantum-control.typ
    ├── tensor-network.typ
    ├── bdd.typ
    ├── feynman.typ
    ├── plot.typ
    └── paper-layout.typ
```

### plugin.json

```json
{
  "name": "inline-viz",
  "description": "Inline terminal visualization for scientific diagrams via typst",
  "version": "0.1.0",
  "author": { "name": "hmyuuu" },
  "keywords": ["visualization", "typst", "terminal", "inline-image", "quantum", "tensor-network", "plotting"]
}
```

### Marketplace Entry (in hmyuuu-skills marketplace.json)

```json
{
  "name": "inline-viz",
  "description": "Inline terminal visualization — render typst diagrams (quantum circuits, tensor networks, QEC codes, BDDs, plots) directly in iTerm2/Kitty/Ghostty",
  "version": "0.1.0",
  "author": { "name": "hmyuuu" },
  "source": "./plugins/inline-viz",
  "category": "visualization"
}
```

---

## Use Cases (Priority Order)

### UC1: Pixel Art — Pipeline Smoke Test
**Package:** pixel-family
**Flow:** Agent writes .typ importing pixel-family → vizrender → characters appear inline → agent reads back SVG to verify render.
**Why first:** Binary pass/fail, validates entire pipeline with zero domain complexity.

### UC2: QEC — Surface Code Decoding
**Package:** qec-thrust
**Flow:** Agent simulates syndrome extraction → writes .typ using qec.typ template with error/correction overlays → vizrender → lattice with highlighted errors displayed inline → agent reads SVG to verify error marker coordinates.
**Example:** Distance-5 surface code, depolarizing noise p=0.01, MWPM decoder, error/correction overlay, logical error rate.

### UC3: Quantum Circuit + Bloch Sphere (Optimal Control)
**Packages:** CeTZ
**Flow:** Agent optimizes GRAPE/DRAG pulse → writes quantum-control.typ with multi-panel layout (circuit | Bloch trajectory with decoherence | pulse waveforms | fidelity sweep) → vizrender → agent verifies all panels rendered correctly.
**Example:** Transmon qubit T1=50μs T2=30μs, DRAG pulse for π/2, Lindblad dynamics, robustness to 5% detuning.

### UC4: Tensor Network — Kitaev Honeycomb
**Packages:** CeTZ
**Flow:** Agent draws honeycomb lattice with 3 bond types (Jx, Jy, Jz) color-coded, line width ∝ coupling strength → overlays iPEPS ansatz with bond dimensions → shows entanglement entropy across cuts.
**Example:** Kitaev honeycomb K_x=1, K_y=1, K_z=0.5, ground state TN ansatz.

### UC5: Binary Decision Diagram
**Package:** typdd
**Flow:** Agent writes boolean expression → renders BDD via typdd → displays inline → re-renders with different variable ordering → side-by-side comparison showing node count difference.
**Example:** 2-bit adder carry: `(a1 & b1) | (a1 & c_in) | (b1 & c_in)`, compare orderings.

### UC6: Feynman Diagrams
**Packages:** CeTZ
**Flow:** Agent identifies relevant diagram → writes feynman.typ with propagator types and vertex labels → renders inline → verifies line styles and momentum labels.
**Example:** QED 1-loop vertex correction (fermion triangle, 2 external fermions + 1 photon).

### UC7: Paper Panel Layout
**Flow:** Agent reads existing figure via vision → proposes alternative panel arrangements → writes paper-layout.typ → renders → user gives feedback ("make c and d equal height") → agent modifies → re-renders → verifies via vision readback.

### UC8: Live MCP Experiment Monitoring
**Flow:** Agent connects to MCP (e.g., dilution fridge T1 monitor) → polls on interval → updates plot.typ with new data points + trend line → vizrender → displays updated plot inline → detects anomalies → highlights in red → alerts user.

---

## Dependencies

### Required
- `typst` CLI (for compilation)

### Optional (fallback chain for SVG→PNG)
- `rsvg-convert` (from librsvg, preferred)
- `magick` (from ImageMagick)
- Falls back to `typst compile --format png` (direct, no SVG intermediate)

### Optional (terminal display tools, used when native protocol detection fails)
- `timg` — multi-protocol support
- `chafa` — multi-protocol support
- `imgcat` — iTerm2 bundled
- `kitten` — Kitty bundled

### Typst Packages (resolved via @preview/)
- `@preview/pixel-family` — pixel art characters
- `@preview/qec-thrust` — QEC code visualization
- `@preview/typdd` — BDD visualization
- `@preview/cetz` — general drawing and plotting

---

## Implementation Order

1. **Scripts first:** vizshow → vizrender (core pipeline)
2. **Smoke test:** pixel-art.typ template → validate end-to-end
3. **SKILL.md:** write skill document with quick start and core workflow
4. **High priority templates:** qec.typ → quantum-control.typ
5. **Medium priority templates:** tensor-network.typ → bdd.typ → feynman.typ
6. **Later templates:** plot.typ → paper-layout.typ
7. **Marketplace integration:** add to hmyuuu-skills marketplace.json, install, test
