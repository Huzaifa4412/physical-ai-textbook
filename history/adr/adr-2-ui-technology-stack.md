# ADR-2: UI Technology Stack for Physical AI Textbook

## Status
Accepted

## Date
2025-12-17

## Context
The Physical AI Textbook project requires a modern, professional UI that appeals to robotics engineers and technical professionals. The UI needs to support both a homepage with specific design requirements and a research assistant chatbot. The solution must be maintainable, have good performance characteristics, and align with the project's static site architecture.

## Decision
We will use the following UI technology stack:
- **Framework**: Docusaurus v3.x with React components
- **Styling**: CSS Modules for component-scoped styling
- **Language**: TypeScript/JavaScript for type safety and modern development
- **Testing**: Jest and React Testing Library for component testing

This approach leverages the existing Docusaurus infrastructure while allowing for custom UI implementations that meet the specific requirements outlined in the feature specification.

## Alternatives Considered
- **Next.js + Tailwind CSS**: Would provide more advanced features but would require significant architectural changes from the existing Docusaurus setup
- **Vanilla HTML/CSS**: Would not leverage existing framework benefits and would require more custom code
- **React with a different static site generator**: Would require migration from the existing Docusaurus setup

## Consequences
### Positive
- Leverages existing Docusaurus infrastructure and ecosystem
- Provides component-based architecture for maintainability
- Supports the required dark theme and professional styling requirements
- Integrates well with the existing documentation workflow
- Provides good performance for static content
- TypeScript support improves code quality and maintainability

### Negative
- Learning curve for Docusaurus-specific patterns
- Less flexibility compared to a fully custom solution
- Dependency on Docusaurus ecosystem for future changes

## References
- `specs/003-physical-ai-ui/plan.md`
- `specs/003-physical-ai-ui/research.md`
- `specs/003-physical-ai-ui/spec.md`