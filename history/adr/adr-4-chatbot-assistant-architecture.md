# ADR-4: Chatbot Assistant Architecture

## Status
Accepted

## Date
2025-12-17

## Context
The Physical AI Textbook needs a research assistant chatbot that helps readers understand humanoids, perception, control, and systems. The chatbot must follow specific UI/UX requirements (floating button, calm tone, no animations) while integrating with the existing RAG system and maintaining the professional, technical tone appropriate for robotics engineers.

## Decision
We will implement a globally mounted chatbot assistant with the following architecture:

### UI/UX Requirements
- Floating button in bottom-right corner
- Never auto-opens (user initiated only)
- Available on all pages via global mount in Root.js
- Title: "Physical AI Assistant"
- Calm, technical tone with no emojis or animations
- Borders preferred over shadows (consistent with design system)

### Integration Approach
- Enhanced existing `src/theme/ChatWidget.js` component
- CSS styling in `src/theme/ChatWidget.css`
- Global mounting via `src/theme/Root.js`
- Integration with existing RAG system per Principle 5 of constitution

### API Contract
- Standardized API contract for communication with backend services
- Session management for conversation continuity
- Metadata tracking for context awareness

This approach maintains architectural consistency while meeting the specific requirements for a professional research assistant.

## Alternatives Considered
- **Always visible chat panel**: Rejected as it would distract from reading experience
- **Page-specific placement**: Rejected as specification requires global availability
- **Consumer-focused chat interface**: Rejected as it doesn't match professional requirements
- **Third-party chat widget**: Rejected as it would not meet specific styling and behavior requirements
- **Separate standalone application**: Rejected as it would break integration with documentation

## Consequences
### Positive
- Consistent availability across all documentation pages
- Professional appearance aligned with design system
- Maintains focus on content while providing assistance
- Integrates well with existing RAG system
- Meets specific requirements for technical audience

### Negative
- Additional complexity in global state management
- Potential performance impact from always-present component
- Need for careful implementation to avoid interfering with reading experience

## References
- `specs/003-physical-ai-ui/plan.md`
- `specs/003-physical-ai-ui/research.md`
- `specs/003-physical-ai-ui/spec.md`
- `specs/003-physical-ai-ui/contracts/chatbot-api.yaml`