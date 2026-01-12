---
name: skill:derivation-checker
description: Verify mathematical derivations step-by-step, checking algebra while human spots physical intuition errors
---

# Derivation Checker (L1 - Conversational)

You are executing the derivation-checker skill.

## User Request
$ARGUMENTS

## Purpose
Check mathematical derivations step-by-step. AI verifies algebra; you catch physics intuition errors AI will miss.

## Autonomy Level: L1 (Conversational)
- **Human**: Provide derivation, spot intuition errors
- **AI**: Check algebra step-by-step, annotate issues

## Workflow

| Phase | Actor | Action |
|-------|-------|--------|
| 1 | **Human** | Provide derivation |
| 2 | Prover | Parse into discrete steps |
| 3 | Prover | Verify each step algebraically |
| 4 | Writer | Annotate errors/gaps found |
| 5 | **Human** | Spot physical intuition issues AI misses |

## Input Required
- Derivation (typst, latex, or plain text)
- Context: what physical system/theory

## Output Format
```markdown
## Step-by-Step Analysis

### Step 1: [equation]
✓ Algebraically correct

### Step 2: [equation]  
⚠ Warning: Sign error in second term
  Expected: -∂H/∂q
  Got: +∂H/∂q

### Step 3: [equation]
? Assumption: assuming commutator [A,B]=0
  Is this justified in your system?
```

## What AI Checks
- Algebraic manipulations
- Index consistency (Einstein notation)
- Dimensional analysis
- Common identities (trig, calculus)

## What Human Must Check
- Physical reasonableness of assumptions
- Boundary conditions make sense
- Order of limits/approximations
- Whether the result "feels right"

## Human Checkpoint
Every step - this is L1, human validates continuously
