---
name: experiment-logger
description: Log ML experiments with hyperparameters, metrics, and plots; human interprets results and plans next experiments
---

# Experiment Logger (L2 - Directed)

## Usage
```
/skill:experiment-logger log run: lr=0.001 batch=32 loss=0.23
/skill:experiment-logger compare exp_001 vs exp_002
```

## Purpose
Track ML experiments systematically. AI logs and visualizes; you interpret and decide next steps.

## Autonomy Level: L2 (Directed)
- **Human**: Define goals, interpret results, plan next experiments
- **AI**: Log params, generate plots, summarize runs

## Workflow

| Phase | Actor | Action |
|-------|-------|--------|
| 1 | **Human** | Define experiment goals |
| 2 | Coder | Set up logging (params, metrics) |
| 3 | Coder | Run experiment |
| 4 | Coder | Generate plots (loss curves, comparisons) |
| 5 | Writer | Summarize results |
| 6 | **Human** | Interpret, decide next experiments |

## Input Required
- Experiment name/description
- Hyperparameters to track
- Metrics to log
- Comparison baseline (optional)

## Log Structure
```
experiments/
├── exp_001_baseline/
│   ├── config.yaml
│   ├── metrics.json
│   ├── plots/
│   │   ├── loss.png
│   │   └── accuracy.png
│   └── summary.md
├── exp_002_lr_sweep/
│   └── ...
└── comparison.md
```

## Output Format
```markdown
# Experiment: [name]

## Config
- learning_rate: 0.001
- batch_size: 32
- epochs: 100

## Results
| Metric | Value | vs Baseline |
|--------|-------|-------------|
| Loss   | 0.23  | -15%        |
| Acc    | 94.2% | +2.1%       |

## Observations
- Converged faster than baseline
- Some overfitting after epoch 80

## Plots
![Loss Curve](plots/loss.png)
```

## Human Checkpoints
1. Are these the right metrics to track?
2. What do results mean for the research question?
3. What experiment to run next?
