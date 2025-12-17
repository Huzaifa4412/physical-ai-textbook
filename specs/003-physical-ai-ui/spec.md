# Feature Specification: Physical AI & Humanoid UI

**Feature Branch**: `003-physical-ai-ui`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "# /sp.specify — Physical AI & Humanoids (Short)

## Goal

Make the Docusaurus home page and chatbot UI **clean, modern, and professional**, suitable for a **technical book on Physical AI & Humanoid Robotics**.

---

## Project Structure Also check it by your own

```
site/
├─ docs/                    # Book content
├─ src/
│  ├─ pages/
│  │  ├─ index.tsx
│  │  └─ index.module.css
│  └─ theme/
│     ├─ ChatWidget.js
│     ├─ ChatWidget.css
│     └─ Root.js            # Global mount
```

---

## Home Page (`src/pages/index.tsx`)

Purpose: Clearly explain what the book is about.

Home Page Structure

1. Hero Section (Above the Fold)

Purpose: Instantly explain that the book is about Physical AI & Humanoid Robotics, not generic software AI.

Layout:

Left aligned text

Right side: abstract humanoid / robotic geometry illustration (wireframe, very low contrast)

Content:

H1 (strong, precise):

\"Physical AI & Humanoid Systems\"

Subtitle (1–2 lines, technical tone):

\"A deep, engineering-focused guide to embodied intelligence, humanoid robots, perception, control, and real-world AI systems.\"

Supporting line (optional):

\"From sensors and simulation to autonomy and deployment.\"

Primary CTA button:

Text: Start Reading

Style: solid accent color

Secondary CTA:

Text: View Book Structure

Style: outline / subtle

Avoid marketing language. Use academic-engineering clarity.

2. Trust & Scope Section

Purpose: Establish credibility and scope.

Grid (3 columns on desktop):

Cards:

Production Focused

Real-world architectures

Deployment-ready patterns

Agentic Systems

OpenAI Agents SDK

Tool calling, memory, workflows

End-to-End

Docs → Embeddings → RAG → UI

Cards must be:

Flat

Soft borders

No shadows or very subtle

Sections (simple, no marketing):

1. **Hero**

   * Title: `Physical AI & Humanoid Systems`
   * Subtitle: embodied intelligence, robotics, real-world AI
   * CTA: `Start Reading`

2. **Book Scope**

   * Physical AI
   * Robot Brain
   * Digital Twin & Simulation
   * ROS2 Nervous System

3. **Learning Path**

   * Foundations → Perception → Planning → Control → Autonomy

Rules:

* Presentational only
* No chatbot logic
* Minimal CSS, lots of whitespace

---

## Chatbot (Research Assistant Style)

Mounted globally in:

```
src/theme/Root.js
```

Behavior:

* Floating button (bottom-right)
* Never auto-open
* Available on all pages

UI Rules:

* Title: `Physical AI Assistant`
* Calm, technical tone
* Borders > shadows
* No emojis, no animations

Purpose:

* Help readers understand humanoids, perception, control, and systems

---

## Color Theme & Styling

**Theme:** Dark, research-grade, robotics-oriented

Colors:

* Background: `#0b0e14` (near-black)
* Surface / panels: `#111827`
* Primary text: `#e5e7eb`
* Secondary text: `#9ca3af`
* Borders / dividers: `#1f2937`
* Accent (only one): `#3b82f6` (blue)
* Accent hover: `#2563eb`

Rules:

* No gradients
* No multiple accent colors
* Prefer borders over shadows
* High contrast for long reading

Typography:

* Font: system-ui or Inter
* Headings: 600–700 weight
* Body: 400 weight
* Max line length ~70ch

---

## Success Criteria

* Looks credible to robotics engineers
* Does not distract from reading
* Explains the book in seconds

**End**"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Professional Book Introduction (Priority: P1)

As a robotics engineer or researcher visiting the website, I want to immediately understand that this book is about Physical AI & Humanoid Robotics, not generic software AI, so that I can determine if the content is relevant to my work.

**Why this priority**: This is the core value proposition of the book and the first impression users have. If users don't understand what the book is about within seconds, they will leave.

**Independent Test**: The homepage clearly communicates "Physical AI & Humanoid Systems" as the main topic with a technical subtitle that explains the focus on embodied intelligence, humanoid robots, perception, control, and real-world AI systems.

**Acceptance Scenarios**:

1. **Given** I am a robotics professional visiting the homepage, **When** I see the hero section, **Then** I immediately understand this book is about Physical AI & Humanoid Robotics and not generic AI/ML

2. **Given** I am a new visitor to the site, **When** I land on the homepage, **Then** I can understand the book's purpose within 3 seconds of viewing the hero section

---

### User Story 2 - Technical Content Discovery (Priority: P1)

As a reader interested in the book's content, I want to see the scope and learning path clearly presented, so that I can understand what topics are covered and how they progress from foundations to advanced concepts.

**Why this priority**: Users need to understand the book's comprehensive coverage to justify spending time reading it. This builds trust and sets expectations.

**Independent Test**: The homepage displays clear sections showing book scope (Physical AI, Robot Brain, Digital Twin & Simulation, ROS2 Nervous System) and a learning path (Foundations → Perception → Planning → Control → Autonomy).

**Acceptance Scenarios**:

1. **Given** I am evaluating the book for my learning needs, **When** I view the scope section, **Then** I can identify the specific technical topics covered

2. **Given** I am interested in the book's structure, **When** I view the learning path, **Then** I can understand the progression from basic to advanced concepts

---

### User Story 3 - Research Assistant Access (Priority: P2)

As a reader studying the book content, I want to access a technical research assistant that can answer questions about humanoids, perception, control, and systems, so that I can get clarifications without leaving the reading experience.

**Why this priority**: This enhances the learning experience by providing immediate access to domain-specific knowledge, making the book more valuable as a reference.

**Independent Test**: A floating "Physical AI Assistant" button appears on all pages that allows users to ask technical questions about the content.

**Acceptance Scenarios**:

1. **Given** I am reading book content and have a question, **When** I click the floating assistant button, **Then** I can ask questions about humanoids, perception, control, and systems

2. **Given** I am using the assistant, **When** I ask a technical question, **Then** I receive responses in a calm, technical tone without marketing language

---

### User Story 4 - Professional Visual Design (Priority: P1)

As a technical professional, I want to see a clean, modern, and professional design with a research-grade aesthetic, so that I trust the content's technical quality.

**Why this priority**: Visual design directly impacts credibility in technical fields. A professional appearance is essential for the target audience of robotics engineers.

**Independent Test**: The site uses a dark theme with specific colors (background: #0b0e14, surface: #111827, accent: #3b82f6) with borders preferred over shadows and high contrast for readability.

**Acceptance Scenarios**:

1. **Given** I am a robotics engineer visiting the site, **When** I view the visual design, **Then** I perceive it as professional and research-grade rather than marketing-focused

2. **Given** I am reading content for extended periods, **When** I view the pages, **Then** the design supports long reading sessions with appropriate contrast and typography

---

### Edge Cases

- What happens when users access the site on mobile devices where the layout needs to adapt?
- How does the chatbot assistant handle questions outside the scope of Physical AI & Humanoid Robotics?
- What occurs when the site is accessed with different screen sizes that affect the hero section layout?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a hero section with "Physical AI & Humanoid Systems" as the main heading
- **FR-002**: System MUST present a technical subtitle: "A deep, engineering-focused guide to embodied intelligence, humanoid robots, perception, control, and real-world AI systems."
- **FR-003**: System MUST include a "Start Reading" primary CTA button with solid accent color
- **FR-004**: System MUST provide a "View Book Structure" secondary CTA button with outline styling
- **FR-005**: System MUST display a trust/scope section with three cards: "Production Focused", "Agentic Systems", and "End-to-End"
- **FR-006**: System MUST implement the specified dark color theme with background #0b0e14 and accent color #3b82f6
- **FR-007**: System MUST display an abstract humanoid/robotic geometry illustration on the right side of the hero section
- **FR-008**: System MUST mount a floating chatbot assistant button in the bottom-right corner of all pages
- **FR-009**: System MUST ensure the chatbot assistant never auto-opens but is available on user interaction
- **FR-010**: System MUST apply typography with headings in 600-700 weight and max line length of ~70ch for readability
- **FR-011**: System MUST ensure the design follows the specified rules: no gradients, no multiple accent colors, borders preferred over shadows
- **FR-012**: System MUST present a learning path section showing: "Foundations → Perception → Planning → Control → Autonomy"
- **FR-013**: System MUST ensure the homepage layout has left-aligned text with an abstract humanoid illustration on the right side
- **FR-014**: System MUST implement flat cards with soft borders and no shadows for the scope section
- **FR-015**: System MUST ensure the chatbot assistant has the title "Physical AI Assistant" with a calm, technical tone

### Key Entities

- **Homepage Content**: The structured information displayed on the main page including hero section, scope cards, and learning path
- **Chat Assistant Interface**: The floating button and associated UI that allows users to interact with the Physical AI Assistant
- **Visual Design System**: The color palette, typography, and styling rules that create the professional, research-grade appearance

## Constitution Alignment *(mandatory)*

- **Professional Design Principle**: This spec adheres to the requirement for a clean, modern, and professional design suitable for technical content in the Physical AI domain.
- **Technical Accuracy Principle**: The spec ensures content is presented with academic-engineering clarity without marketing language, aligning with technical accuracy requirements.
- **User Experience Principle**: The spec prioritizes the needs of robotics engineers and technical professionals by focusing on credibility and clarity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 90% of robotics engineers who visit the homepage understand within 3 seconds that the book is about Physical AI & Humanoid Robotics (not generic software AI)
- **SC-002**: The homepage design receives credibility ratings of 4+ out of 5 from target audience of robotics professionals
- **SC-003**: Users spend at least 2 minutes on the homepage exploring content and book structure
- **SC-004**: The chatbot assistant is accessed by at least 30% of users during their visit to get clarifications on technical topics
- **SC-005**: Page load times remain under 3 seconds while maintaining the professional visual design
