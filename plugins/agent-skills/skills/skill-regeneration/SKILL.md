---
name: skill-regeneration
description: Update skills with concise concrete practices, keeping SKILL.md minimal
---

# Skill Regeneration (L2 - Directed)

You are executing the skill-regeneration skill.

## User Request
$ARGUMENTS

## Purpose
Refine and update existing skills based on concrete practices learned during execution. Keep skill definitions minimal and actionable.

## Autonomy Level: L2 (Directed)
- **Trigger**: Manual only (human-initiated)
- **Human**: Provide practice insights, approve changes
- **AI**: Analyze → distill → update → validate

## Agent Loop
```
while not goal_reached:
    researcher.read_target_skill()
    researcher.analyze_practice_log(concrete_examples)
    writer.distill_to_minimal_patterns()
    coder.update_skill_md(target_skill)
    human_checkpoint("Review skill update")
```

## Input Required
- Target skill name to update
- Concrete practice examples or session logs
- (Optional) Specific sections to refine

## Principles
1. **Concise over comprehensive** - Remove redundant explanations
2. **Concrete over abstract** - Real examples beat theory
3. **Actionable over descriptive** - Steps beat prose
4. **Patterns over instances** - Generalize from specifics

## Output
Updated SKILL.md with:
- Tighter agent loop
- Refined checkpoints
- Distilled patterns from practice

## Human Checkpoint
- Review diff of skill changes
- Confirm patterns match intent

## Output
- PR to skills repo with updated SKILL.md
