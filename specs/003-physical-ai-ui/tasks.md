# Implementation Tasks: Physical AI & Humanoid UI

**Feature**: Physical AI & Humanoid UI | **Branch**: `003-physical-ai-ui` | **Date**: 2025-12-17
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Implementation Strategy

This feature implements a clean, modern, and professional Docusaurus home page and chatbot UI suitable for a technical book on Physical AI & Humanoid Robotics. The implementation follows a user-story-driven approach with P1 stories implemented first, followed by P2. Each story is independently testable and delivers value.

**MVP Scope**: User Story 1 (Professional Book Introduction) provides the core homepage with hero section and CTAs.

## Dependencies

User stories are prioritized as follows:
- US1: Professional Book Introduction (P1) - Independent
- US2: Technical Content Discovery (P1) - Depends on US1 (uses same homepage)
- US4: Professional Visual Design (P1) - Can be implemented in parallel with US1/US2
- US3: Research Assistant Access (P2) - Independent but enhances other stories

## Parallel Execution Examples

- T001-T004 (Setup) can run before any user story
- T005-T010 (Foundational) can run before user stories
- US1 (T011-T020), US2 (T021-T030), and US4 (T031-T040) can run in parallel
- US3 (T041-T050) can run in parallel with other stories

---

## Phase 1: Setup

**Goal**: Prepare development environment and project structure for UI implementation.

- [ ] T001 Set up development environment with Node.js 18+, npm, and Git
- [ ] T002 Navigate to site directory and install Docusaurus dependencies
- [ ] T003 Verify development server starts correctly with `npm start`
- [x] T004 Create backup of original index.tsx and index.module.css files

---

## Phase 2: Foundational

**Goal**: Implement foundational styling and configuration needed across all user stories.

- [x] T005 [P] Create global CSS theme variables for dark theme colors in src/css/custom.css
- [x] T006 [P] Implement dark theme configuration with background: #0b0e14, surface: #111827, primary text: #e5e7eb, secondary text: #9ca3af, borders: #1f2937, accent: #3b82f6, accent hover: #2563eb
- [x] T007 [P] Set up typography system with system-ui or Inter font, headings 600-700 weight, body 400 weight, max line length ~70ch
- [x] T008 [P] Create reusable CSS module for card styling with flat design, soft borders, no shadows
- [x] T009 [P] Create reusable CSS module for button styling with solid accent color for primary CTA and outline style for secondary CTA
- [x] T010 [P] Set up responsive grid system for 3-column layout on desktop

---

## Phase 3: User Story 1 - Professional Book Introduction (Priority: P1)

**Goal**: Implement hero section that immediately explains the book is about Physical AI & Humanoid Robotics, not generic software AI.

**Independent Test**: The homepage clearly communicates "Physical AI & Humanoid Systems" as the main topic with a technical subtitle that explains the focus on embodied intelligence, humanoid robots, perception, control, and real-world AI systems.

- [x] T011 [US1] Update index.tsx to implement hero section with left-aligned text layout
- [x] T012 [US1] Add H1 heading "Physical AI & Humanoid Systems" to hero section
- [x] T013 [US1] Add technical subtitle: "A deep, engineering-focused guide to embodied intelligence, humanoid robots, perception, control, and real-world AI systems."
- [x] T014 [US1] Add optional supporting line: "From sensors and simulation to autonomy and deployment."
- [x] T015 [P] [US1] Create primary CTA button with text "Start Reading" and solid accent color style
- [x] T016 [P] [US1] Create secondary CTA button with text "View Book Structure" and outline/subtle style
- [x] T017 [P] [US1] Add abstract humanoid/robotic geometry illustration on right side of hero section
- [x] T018 [P] [US1] Apply dark theme styling to hero section with specified colors
- [x] T019 [P] [US1] Ensure hero section layout has left-aligned text with illustration on right side
- [ ] T020 [US1] Test that hero section meets acceptance criteria: robotics professionals understand the book topic within 3 seconds

---

## Phase 4: User Story 2 - Technical Content Discovery (Priority: P1)

**Goal**: Display scope and learning path clearly so users understand what topics are covered and how they progress from foundations to advanced concepts.

**Independent Test**: The homepage displays clear sections showing book scope (Physical AI, Robot Brain, Digital Twin & Simulation, ROS2 Nervous System) and a learning path (Foundations → Perception → Planning → Control → Autonomy).

- [x] T021 [US2] Create trust & scope section below hero section in index.tsx
- [x] T022 [P] [US2] Create first card with title "Production Focused" and description "Real-world architectures, deployment-ready patterns"
- [x] T023 [P] [US2] Create second card with title "Agentic Systems" and description "OpenAI Agents SDK, tool calling, memory, workflows"
- [x] T024 [P] [US2] Create third card with title "End-to-End" and description "Docs → Embeddings → RAG → UI"
- [x] T025 [P] [US2] Apply flat card design with soft borders and no shadows as specified
- [x] T026 [US2] Create learning path section with "Foundations → Perception → Planning → Control → Autonomy" progression
- [x] T027 [P] [US2] Add detailed descriptions for each learning path step: Physical AI, Robot Brain, Digital Twin & Simulation, ROS2 Nervous System
- [x] T028 [P] [US2] Style scope section with dark theme colors and professional typography
- [x] T029 [P] [US2] Ensure grid layout works responsively for 3 columns on desktop
- [x] T030 [US2] Test that users can identify specific technical topics covered and understand progression from basic to advanced concepts

---

## Phase 5: User Story 4 - Professional Visual Design (Priority: P1)

**Goal**: Implement clean, modern, and professional design with research-grade aesthetic so technical professionals trust the content's quality.

**Independent Test**: The site uses a dark theme with specific colors (background: #0b0e14, surface: #111827, accent: #3b82f6) with borders preferred over shadows and high contrast for readability.

- [x] T031 [US4] Apply dark theme background (#0b0e14) to entire site
- [x] T032 [P] [US4] Apply surface color (#111827) to panels and containers
- [x] T033 [P] [US4] Apply primary text color (#e5e7eb) to main content
- [x] T034 [P] [US4] Apply secondary text color (#9ca3af) to supporting text
- [x] T035 [P] [US4] Apply border color (#1f2937) to dividers and card borders
- [x] T036 [P] [US4] Apply accent color (#3b82f6) to primary CTAs and interactive elements
- [x] T037 [P] [US4] Implement accent hover color (#2563eb) for interactive states
- [x] T038 [US4] Ensure no gradients are used anywhere in the UI
- [x] T039 [US4] Ensure only the single accent color is used (no multiple accent colors)
- [x] T040 [US4] Test that design meets high contrast requirements for long reading sessions

---

## Phase 6: User Story 3 - Research Assistant Access (Priority: P2)

**Goal**: Provide access to a technical research assistant that can answer questions about humanoids, perception, control, and systems without leaving the reading experience.

**Independent Test**: A floating "Physical AI Assistant" button appears on all pages that allows users to ask technical questions about the content.

- [x] T041 [US3] Update Root.js to globally mount the chatbot assistant
- [x] T042 [P] [US3] Create floating button component for chat assistant
- [x] T043 [P] [US3] Position floating button in bottom-right corner of all pages
- [x] T044 [P] [US3] Ensure chatbot never auto-opens (user initiated only)
- [x] T045 [P] [US3] Set chatbot title to "Physical AI Assistant"
- [x] T046 [P] [US3] Implement calm, technical tone styling for chat interface
- [x] T047 [P] [US3] Ensure no emojis or animations in chatbot UI
- [x] T048 [P] [US3] Implement borders > shadows design approach for chat widget
- [x] T049 [P] [US3] Connect chat widget to API endpoints per contract specification
- [x] T050 [US3] Test that users can access the assistant and ask questions about humanoids, perception, control, and systems

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Final touches, responsive design, performance optimization, and quality assurance.

- [ ] T051 Implement responsive design for mobile devices to handle layout adaptation
- [ ] T052 Optimize page load time to remain under 3 seconds with professional visual design
- [ ] T053 Add proper alt text and accessibility attributes to all UI elements
- [ ] T054 Test all UI elements across different screen sizes affecting hero section layout
- [ ] T055 Verify all functional requirements (FR-001 to FR-015) are implemented
- [ ] T056 Test that chatbot handles questions outside Physical AI & Humanoid Robotics scope appropriately
- [ ] T057 Implement error handling and fallbacks for all UI components
- [ ] T058 Verify all success criteria (SC-001 to SC-005) are met
- [ ] T059 Run accessibility audit and fix any issues found
- [ ] T060 Final end-to-end testing of all user stories and acceptance scenarios