# LaTeX to Typst

Convert LaTeX documents and equations to typst format.

## User Request
$ARGUMENTS

## Conversions
| LaTeX | Typst |
|-------|-------|
| `\section{X}` | `= X` |
| `$...$` | `$...$` |
| `\frac{a}{b}` | `a/b` |
| `\sqrt{x}` | `sqrt(x)` |
| `\cite{ref}` | `@ref` |

## Tool
```bash
./latex2typst -i input.tex -o output.typ
```
