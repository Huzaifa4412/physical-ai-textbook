# Research: Physical AI & Humanoid UI

## Overview
This document captures research findings for the Physical AI & Humanoid UI feature implementation. It addresses all technical decisions and unknowns identified during the planning phase.

## Homepage Design Implementation

### Decision: Homepage Structure
**What was chosen**: Implement a hero section with left-aligned text and right-side abstract humanoid illustration, followed by trust/scope section with 3-column grid layout.

**Rationale**: This layout matches the specification requirements and provides a clean, professional appearance suitable for technical content. The left-aligned text ensures readability while the right-side illustration provides visual interest without distraction.

**Alternatives considered**:
- Centered layout: Rejected as it could reduce readability for technical content
- Full-width sections: Rejected as it doesn't match the specified design requirements

### Decision: Color Theme Implementation
**What was chosen**: Implement dark theme with specific colors (background: #0b0e14, surface: #111827, accent: #3b82f6) as specified in the feature requirements.

**Rationale**: The dark theme supports long reading sessions with high contrast, and the specific colors create a research-grade, robotics-oriented aesthetic appropriate for the target audience.

**Alternatives considered**:
- Light theme: Rejected as it doesn't match the specification and isn't optimal for long reading sessions
- Multiple accent colors: Rejected as specification requires only one accent color
- Gradients: Rejected as specification explicitly prohibits gradients

### Decision: Typography and Layout
**What was chosen**: System-ui or Inter font with headings 600-700 weight, body 400 weight, max line length ~70ch as specified.

**Rationale**: These typography choices support the professional, research-grade appearance and ensure readability during long reading sessions.

## Chatbot Assistant Implementation

### Decision: Chatbot UI Placement
**What was chosen**: Floating button in bottom-right corner, mounted globally in Root.js, never auto-open, available on all pages.

**Rationale**: This follows common patterns for chat assistants while meeting the specific requirements in the feature specification.

**Alternatives considered**:
- Always visible chat panel: Rejected as it would distract from reading
- Page-specific placement: Rejected as specification requires global availability

### Decision: Chatbot Styling
**What was chosen**: Calm, technical tone with borders > shadows, no emojis, no animations as specified.

**Rationale**: This maintains the professional, research-grade aesthetic appropriate for the target audience of robotics engineers.

**Alternatives considered**:
- Consumer-focused chat interface: Rejected as it doesn't match the professional requirements
- Animated elements: Rejected as specification prohibits animations

## Technical Implementation Approach

### Decision: Docusaurus Homepage Customization
**What was chosen**: Modify existing `src/pages/index.tsx` and `src/pages/index.module.css` files to implement the new design.

**Rationale**: This follows Docusaurus conventions and leverages the existing framework while meeting all specified requirements.

**Alternatives considered**:
- Creating a new page component: Rejected as the specification specifically targets the existing index page
- Using Docusaurus presets only: Rejected as custom design is required to meet specifications

### Decision: Chat Widget Development
**What was chosen**: Enhance existing `src/theme/ChatWidget.js` and `ChatWidget.css` files with the new styling and behavior requirements.

**Rationale**: This maintains the existing architecture while implementing the required changes for the professional appearance.

**Alternatives considered**:
- Replacing with third-party chat widget: Rejected as it would not meet the specific styling requirements
- Creating entirely new component: Rejected as it would duplicate existing functionality unnecessarily