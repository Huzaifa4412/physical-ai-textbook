# ADR-3: Design System and Styling Approach

## Status
Accepted

## Date
2025-12-17

## Context
The Physical AI Textbook requires a professional, research-grade aesthetic that appeals to robotics engineers. The design must follow specific requirements including a dark theme with precise colors, typography rules, and visual guidelines that prioritize readability and technical credibility over marketing appeal. The styling approach needs to be consistent across both the homepage and chatbot UI.

## Decision
We will implement a strict design system with the following characteristics:

### Color Palette
- Background: `#0b0e14` (near-black)
- Surface/panels: `#111827`
- Primary text: `#e5e7eb`
- Secondary text: `#9ca3af`
- Borders/dividers: `#1f2937`
- Accent (only one): `#3b82f6` (blue)
- Accent hover: `#2563eb`

### Typography
- Font: system-ui or Inter
- Headings: 600-700 weight
- Body: 400 weight
- Max line length: ~70ch for readability

### Styling Rules
- No gradients
- No multiple accent colors
- Borders preferred over shadows
- High contrast for long reading sessions
- Calm, technical tone for all UI elements

This approach ensures visual consistency and meets the professional requirements specified for the target audience.

## Alternatives Considered
- **Light theme**: Rejected as it doesn't meet the specified requirements and isn't optimal for long reading sessions
- **Multiple accent colors**: Rejected as specification requires only one accent color
- **Consumer-focused design**: Rejected as it doesn't match the professional requirements for technical audience
- **Gradient and shadow-heavy design**: Rejected as specification explicitly prohibits gradients and prefers borders

## Consequences
### Positive
- Creates a professional, research-grade appearance appropriate for technical audience
- High contrast supports long reading sessions
- Consistent visual language across all UI elements
- Meets specific requirements outlined in feature specification
- Maintains credibility with target audience of robotics engineers

### Negative
- Less visual variety due to single accent color constraint
- Dark theme may not be preferred by all users
- Strict design constraints limit creative flexibility

## References
- `specs/003-physical-ai-ui/plan.md`
- `specs/003-physical-ai-ui/research.md`
- `specs/003-physical-ai-ui/spec.md`