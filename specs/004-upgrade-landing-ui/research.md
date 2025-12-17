# Research: Upgrade Landing Page UI

## Decision: Color Theme Implementation
**Rationale:** The specified dark robotics-oriented theme aligns with the existing custom.css colors, which already define:
- Background: #0b0e14
- Surface: #111827
- Primary text: #e5e7eb
- Secondary text: #9ca3af
- Borders: #1f2937
- Accent: #3b82f6
- Accent hover: #2563eb

**Alternatives considered:**
- Light theme (rejected - doesn't match requirement for "research-grade" feel)
- Different color schemes (rejected - the current scheme already matches requirements)

## Decision: Typography Implementation
**Rationale:** The existing custom.css already defines system-ui font family with appropriate weights. Need to ensure headings use 600-700 weight and body text uses 400 weight. Max line width of ~70ch is already configured via --ifm-max-width: 70ch.

**Alternatives considered:**
- Custom fonts (rejected - system-ui provides better performance and accessibility)

## Decision: Component Structure
**Rationale:** The landing page needs to be restructured to include:
1. Updated Navbar with sticky positioning and proper links
2. Hero section with specified content
3. Feature cards section (4 cards as specified)
4. Bento grid section for core topics
5. Learning path section
6. "Who This Book Is For" section
7. Updated footer

**Alternatives considered:**
- Single page vs multiple components (chosen to use Docusaurus components approach for maintainability)

## Decision: Accessibility Implementation
**Rationale:** All UI elements must pass WCAG 2.1 AA compliance. This includes proper ARIA attributes, keyboard navigation, and contrast ratios.

**Alternatives considered:**
- Minimal accessibility (rejected - requirement specifies compliance)