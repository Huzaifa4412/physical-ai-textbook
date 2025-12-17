# Feature Specification: Upgrade Landing Page UI

**Feature Branch**: `004-upgrade-landing-ui`
**Created**: 2025-12-18
**Status**: Draft
**Input**: User description: "Upgrade the entire landing page UI (Navbar, Hero, Sections, Footer) to look modern, clean, and research-grade, suitable for a technical book on Physical AI & Humanoid Robotics. This must feel like serious engineering documentation, not a marketing website."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Professional Researcher Visits Site (Priority: P1)

A robotics researcher or engineer visits the landing page to quickly understand what the book is about and whether it's relevant to their work. They need to immediately grasp that this is a technical book about Physical AI and Humanoid Systems, not a marketing website.

**Why this priority**: This is the primary user journey - if visitors don't immediately understand the book's technical nature and relevance, they'll leave.

**Independent Test**: The redesigned landing page should clearly communicate the book's technical nature within 3 seconds of landing, with a clear call-to-action for reading the book.

**Acceptance Scenarios**:

1. **Given** a robotics researcher lands on the page, **When** they view the hero section, **Then** they immediately understand this is a technical book about Physical AI & Humanoid Systems
2. **Given** a user wants to start reading, **When** they click the "Start Reading" button, **Then** they are taken to the book's documentation
3. **Given** a user wants to understand the book structure, **When** they click the "View Structure" button, **Then** they see the book's table of contents or outline

---

### User Story 2 - Engineer Explores Core Topics (Priority: P2)

An engineer exploring the landing page wants to quickly understand the core topics covered in the book to determine if it addresses their specific technical needs.

**Why this priority**: Helps users evaluate if the book contains relevant content for their work.

**Independent Test**: The core topics section should clearly communicate the technical depth and breadth of the book.

**Acceptance Scenarios**:

1. **Given** a user scrolls to the core topics section, **When** they view the bento grid, **Then** they can quickly identify key technical areas covered in the book

---

### User Story 3 - Student Evaluates Learning Path (Priority: P3)

An advanced student wants to understand the learning progression and whether the book is appropriate for their skill level.

**Why this priority**: Helps students determine if the book matches their learning goals.

**Independent Test**: The learning path section should clearly show the progression from foundations to advanced topics.

**Acceptance Scenarios**:

1. **Given** a student views the learning path section, **When** they read the topic sequence, **Then** they understand the progression from basic to advanced concepts

---

## Edge Cases

- What happens when the page is viewed on different screen sizes?
- How does the page handle when users have reduced motion preferences?
- What happens when users navigate with keyboard only?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a professional, research-grade landing page with dark robotics-oriented theme using specified colors (Background: #0b0e14, Surface: #111827, Primary text: #e5e7eb, Secondary text: #9ca3af, Borders: #1f2937, Accent: #3b82f6)
- **FR-002**: System MUST implement a sticky navbar with site title on left and Docs, Book Structure, and GitHub links on right
- **FR-003**: System MUST display hero section with "Physical AI & Humanoid Systems" heading and "embodied intelligence, robotics, real-world AI" subtitle
- **FR-004**: System MUST display feature cards highlighting Physical AI First, Humanoid Systems, Simulation → Reality, and Systems Thinking with their specified descriptions
- **FR-005**: System MUST display a bento grid with core topics: Robot Brain Architecture, Perception & Sensor Fusion, Planning & Control, ROS2 Nervous System, Digital Twins, and Autonomy & Behavior
- **FR-006**: System MUST display a learning path section with Foundations, Perception, World Modeling, Planning & Control, Autonomy, and Sim-to-Real
- **FR-007**: System MUST display a "Who This Book Is For" section targeting engineers, researchers, and advanced students
- **FR-008**: System MUST display a professional footer with book title, description, and navigation links
- **FR-009**: System MUST implement typography with system-ui or Inter font, headings 600-700 weight, body 400 weight
- **FR-010**: System MUST limit max line width to ~70ch for readability
- **FR-011**: System MUST use borders over shadows for visual separation
- **FR-012**: System MUST implement minimal interactions with optional subtle fades only
- **FR-013**: System MUST ensure all UI components use surface background with subtle borders and no shadows
- **FR-014**: System MUST implement consistent spacing and alignment across all sections

### Key Entities *(include if feature involves data)*

- **Landing Page Content**: Represents the visual elements and information displayed on the landing page, including hero text, feature descriptions, and navigation elements
- **UI Components**: Represents the reusable visual elements such as cards, grids, navigation bars, and buttons that make up the landing page

## Constitution Alignment *(mandatory)*

- **PRINCIPLE: Professional Design**: This spec adheres to the principle of creating a research-grade, professional interface suitable for technical documentation as specified in the project constitution.
- **PRINCIPLE: User-Centric Approach**: The requirements prioritize the needs of robotics engineers and researchers who expect clean, technical documentation over marketing-style presentation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users spend at least 30 seconds on the landing page (indicating engagement with the content)
- **SC-002**: 80% of users can identify the book's technical nature within 5 seconds of viewing the page
- **SC-003**: Click-through rate to "Start Reading" button is at least 10% of page visitors
- **SC-004**: Users rate the landing page as "professional and credible" in 85% of feedback surveys
- **SC-005**: Page loads in under 2 seconds on standard internet connections
- **SC-006**: All UI elements pass accessibility standards (WCAG 2.1 AA compliance)
- **SC-007**: The landing page successfully conveys the technical nature of the book to robotics engineers and researchers