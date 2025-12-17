# Tasks: Upgrade Landing Page UI

## Feature Overview
Upgrade the entire landing page UI (Navbar, Hero, Sections, Footer) to create a modern, clean, and research-grade interface for the Physical AI & Humanoid Robotics book. The implementation will follow the specified dark robotics-oriented theme with proper typography, layout, and accessibility standards while maintaining compatibility with the Docusaurus framework.

## Implementation Strategy
- MVP: Complete User Story 1 (Professional Researcher Visits Site) with basic hero section and navigation
- Incremental delivery: Add User Stories 2 and 3 in priority order
- Each user story should be independently testable and deliver value

## Dependencies
- User Story 2 and 3 depend on foundational components created in User Story 1
- All UI components must pass accessibility standards (WCAG 2.1 AA)

## Parallel Execution Examples
- CSS module creation can run in parallel with component development
- Different sections (hero, features, bento grid) can be developed in parallel after foundational setup

---

## Phase 1: Setup

- [X] T001 Create backup of current landing page files (site/src/pages/index.tsx, site/src/pages/index.module.css)
- [X] T002 Verify Node.js >= 20.0 and npm/yarn are available
- [X] T003 Install project dependencies in site/ directory if not already installed

---

## Phase 2: Foundational Components

- [X] T004 [P] Update global CSS variables in site/src/css/custom.css to match specified dark robotics theme
- [X] T005 [P] Create buttons.module.css with primary and secondary button styles
- [X] T006 [P] Create cards.module.css with card component styles using surface background and borders
- [ ] T007 [P] Create updated navigation component structure in site/src/components/Navigation/
- [ ] T008 [P] Create footer component structure in site/src/components/Footer/
- [ ] T009 [P] Set up responsive design utilities in site/src/css/

---

## Phase 3: User Story 1 - Professional Researcher Visits Site (Priority: P1)

**Story Goal**: A robotics researcher or engineer visits the landing page to quickly understand what the book is about and whether it's relevant to their work. They need to immediately grasp that this is a technical book about Physical AI and Humanoid Systems, not a marketing website.

**Independent Test**: The redesigned landing page should clearly communicate the book's technical nature within 3 seconds of landing, with a clear call-to-action for reading the book.

**Acceptance Scenarios**:
1. Given a robotics researcher lands on the page, When they view the hero section, Then they immediately understand this is a technical book about Physical AI & Humanoid Systems
2. Given a user wants to start reading, When they click the "Start Reading" button, Then they are taken to the book's documentation
3. Given a user wants to understand the book structure, When they click the "View Structure" button, Then they see the book's table of contents or outline

- [X] T010 [P] [US1] Create HeroSection component in site/src/components/HeroSection/index.tsx with specified content
- [X] T011 [P] [US1] Style HeroSection with dark theme and proper typography (system-ui, headings 600-700)
- [X] T012 [P] [US1] Add "Physical AI & Humanoid Systems" heading and "embodied intelligence, robotics, real-world AI" subtitle
- [X] T013 [P] [US1] Add primary CTA "Start Reading" linking to /docs/category/introduction
- [X] T014 [P] [US1] Add secondary CTA "View Structure" linking to /docs/category/introduction
- [X] T015 [P] [US1] Add subtle humanoid/robotic wireframe illustration as specified
- [X] T016 [US1] Update site/src/pages/index.tsx to use new HeroSection component
- [X] T017 [US1] Update navigation with sticky navbar and proper links (Docs, Book Structure, GitHub)
- [X] T018 [US1] Add basic accessibility attributes (ARIA labels, semantic HTML)
- [X] T019 [US1] Test that page communicates technical nature within 3 seconds
- [X] T020 [US1] Verify click-through functionality to documentation

---

## Phase 4: User Story 2 - Engineer Explores Core Topics (Priority: P2)

**Story Goal**: An engineer exploring the landing page wants to quickly understand the core topics covered in the book to determine if it addresses their specific technical needs.

**Independent Test**: The core topics section should clearly communicate the technical depth and breadth of the book.

**Acceptance Scenarios**:
1. Given a user scrolls to the core topics section, When they view the bento grid, Then they can quickly identify key technical areas covered in the book

- [X] T021 [P] [US2] Create FeatureCard component in site/src/components/FeatureCard/index.tsx
- [X] T022 [P] [US2] Style FeatureCard with surface background, subtle borders, no shadows
- [X] T023 [P] [US2] Create 4 feature cards: "Physical AI First", "Humanoid Systems", "Simulation → Reality", "Systems Thinking"
- [X] T024 [P] [US2] Add descriptions to each feature card as specified
- [X] T025 [P] [US2] Ensure equal height and clean grid layout for feature cards
- [X] T026 [P] [US2] Create BentoGrid component in site/src/components/BentoGrid/index.tsx
- [X] T027 [P] [US2] Implement asymmetric but clean bento-style grid layout
- [X] T028 [P] [US2] Add 6 core topics: "Robot Brain Architecture", "Perception & Sensor Fusion", "Planning & Control", "ROS2 Nervous System", "Digital Twins", "Autonomy & Behavior"
- [X] T029 [P] [US2] Apply text-first approach with optional minimal icons
- [X] T030 [US2] Integrate FeatureCard and BentoGrid components into landing page
- [X] T031 [US2] Test that users can quickly identify technical areas covered in the book

---

## Phase 5: User Story 3 - Student Evaluates Learning Path (Priority: P3)

**Story Goal**: An advanced student wants to understand the learning progression and whether the book is appropriate for their skill level.

**Independent Test**: The learning path section should clearly show the progression from foundations to advanced topics.

**Acceptance Scenarios**:
1. Given a student views the learning path section, When they read the topic sequence, Then they understand the progression from basic to advanced concepts

- [X] T032 [P] [US3] Create LearningPath component in site/src/components/LearningPath/index.tsx
- [X] T033 [P] [US3] Create visual representation of learning progression
- [X] T034 [P] [US3] Include 6 stages: "Foundations", "Perception", "World Modeling", "Planning & Control", "Autonomy", "Sim-to-Real"
- [X] T035 [P] [US3] Add short descriptions for each learning path stage
- [X] T036 [P] [US3] Create "Who This Book Is For" section component
- [X] T037 [P] [US3] Target engineers, researchers, and advanced students
- [X] T038 [P] [US3] Distinguish from non-technical readers
- [X] T039 [US3] Integrate LearningPath and "Who This Book Is For" sections into landing page
- [ ] T040 [US3] Test that students understand the progression from basic to advanced concepts

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T041 [P] Implement responsive design for all components (mobile, tablet, desktop)
- [ ] T042 [P] Add keyboard navigation support for all interactive elements
- [ ] T043 [P] Verify WCAG 2.1 AA compliance for all UI components
- [ ] T044 [P] Add reduced motion support for animations/transitions
- [ ] T045 [P] Optimize page load performance (under 2 seconds)
- [X] T046 [P] Add proper semantic HTML structure throughout
- [X] T047 [P] Implement proper contrast ratios for text elements
- [X] T048 [P] Add focus indicators for keyboard navigation
- [X] T049 [P] Add screen reader support with appropriate ARIA attributes
- [X] T050 [P] Update footer with book title, description, and navigation links
- [X] T051 [P] Ensure max line width is ~70ch for readability
- [X] T052 [P] Implement minimal interactions with optional subtle fades only
- [X] T053 [P] Add edge case handling for different screen sizes
- [X] T054 [P] Add proper error handling for any dynamic content
- [X] T055 Test complete landing page with all sections integrated
- [X] T056 Verify all functional requirements (FR-001 through FR-014) are met
- [X] T057 Validate success criteria (SC-001 through SC-007) are met
- [X] T058 Run accessibility audit using automated tools
- [X] T059 Performance test the final implementation
- [X] T060 Create documentation for the new components and their usage