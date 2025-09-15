# claudook/choices-enable

Enable A/B/C multiple choice options for complex decisions.

## Usage
```bash
python3 .claude/hooks/claudook/toggle_controls.py enable-choices
```

## What it does:
When enabled, Claude will present multiple implementation approaches for complex tasks, allowing you to choose the best path before proceeding.

## Example scenario:
When asked to implement a feature, Claude presents:
- **Option A**: Quick prototype (minimal viable implementation)
- **Option B**: Balanced approach (good performance vs complexity trade-off)
- **Option C**: Production-ready (full-featured with tests and documentation)

## Benefits:
- Better control over implementation complexity
- Clear understanding of trade-offs
- Ability to choose based on project needs
- Prevents over-engineering or under-delivering

## To disable:
Use `/claudook/choices-disable`
