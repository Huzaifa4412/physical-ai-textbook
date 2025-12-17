---
id: 1
title: upgrade-landing-ui-spec
stage: spec
date: 2025-12-18
surface: agent
model: claude-sonnet-4-5-20250929
feature: upgrade-landing-ui
branch: 004-upgrade-landing-ui
user: claude
command: /sp.specify
labels: ["ui", "landing-page", "specification"]
links:
  spec: specs/004-upgrade-landing-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-upgrade-landing-ui/spec.md
 - specs/004-upgrade-landing-ui/checklists/requirements.md
tests:
 - specs/004-upgrade-landing-ui/spec.md validated against quality checklist
---

## Prompt

## Objective
Upgrade the **entire landing page UI** (Navbar, Hero, Sections, Footer) to look **modern, clean, and research‑grade**, suitable for a **technical book on Physical AI & Humanoid Robotics**.
This must feel like **serious engineering documentation**, not a marketing website.
---
## Entire book directory is /site
## Scope
Affects only:
* Landing page UI
* Navbar (top navigation)
* Footer
Does NOT affect:
* Docs content (`/docs`)
* Chatbot logic
---
## Color Theme
Dark, robotics‑oriented theme:
* Background: `#0b0e14`
* Surface: `#111827`
* Primary text: `#e5e7eb`
* Secondary text: `#9ca3af`
* Borders: `#1f2937`
* Accent (single): `#3b82f6`
* Accent hover: `#2563eb`
Rules:

* One accent only
* No gradients
* Borders over shadows

---

## Typography

* Font: system-ui or Inter
* Headings: 600–700
* Body: 400
* Max line width: ~70ch

---

## Navbar

Purpose: Calm, professional navigation.

Structure:

* Left: Site / Book title
* Right: Links

  * Docs
  * Book Structure
  * GitHub

Rules:

* Sticky but minimal height
* Transparent or surface background
* Bottom border only
* No animations

---

## Hero Section

Purpose: Instantly explain the book.

Content:

* H1: `Physical AI & Humanoid Systems`
* Subtitle: embodied intelligence, robotics, real‑world AI
* Optional support line: robot brains → deployment

CTAs:

* Primary: Start Reading
* Secondary: View Structure

Layout:

* Centered or left‑aligned
* Optional subtle humanoid / robotic wireframe

---

## Landing Sections

### 1. Features (Cards)

Purpose: Highlight core strengths at a glance.

Layout:

* 3 or 4 feature cards
* Equal height
* Clean grid

Feature cards:

* **Physical AI First**

  * Intelligence grounded in physics and embodiment

* **Humanoid Systems**

  * Robot brains, perception, locomotion, manipulation

* **Simulation → Reality**

  * Digital twins, sim-to-real transfer

* **Systems Thinking**

  * End-to-end pipelines, not isolated models

Card rules:

* Surface background
* Subtle border
* No shadows

---

### 2. Bento Grid (Core Topics)

Purpose: Visually communicate depth and structure.

Layout:

* Bento-style grid (asymmetric but clean)
* 4–6 blocks

Blocks:

* Robot Brain Architecture
* Perception & Sensor Fusion
* Planning & Control
* ROS2 Nervous System
* Digital Twins
* Autonomy & Behavior

Rules:

* Text-first
* Optional minimal icon
* No images required

---

### 3. Learning Path

* Foundations
* Perception
* World Modeling
* Planning & Control
* Autonomy
* Sim-to-Real

Short descriptions only.

---

### 4. Who This Book Is For

Good fit:

* Engineers, researchers, advanced students

Not a fit:

* Non-technical readers

---

## Footer

Purpose: Quiet, professional closure.

Content:

* Book title
* Short description (1 line)
* Links:

  * Docs
  * GitHub
  * License / About

Rules:

* No newsletter
* No heavy visuals
* Top border only

---

## Interaction Rules

* No heavy animations
* Optional subtle fade only
* Fast load, minimal JS

---

## Implementation Notes

* Home page: `src/pages/index.tsx`
* Styles: `index.module.css`
* Navbar/Footer via Docusaurus theme or CSS override
* Presentational only

---

## Success Criteria

* Feels credible to robotics engineers
* Calm and readable
* Explains the book quickly
* Consistent across navbar, content, and footer

**End of specification**

## Response snapshot

Created a comprehensive specification for upgrading the landing page UI to create a modern, research-grade interface for the Physical AI & Humanoid Robotics book. The specification includes:

- User scenarios for researchers, engineers, and students
- Functional requirements covering all UI elements (navbar, hero, feature cards, bento grid, learning path, footer)
- Success criteria with measurable outcomes
- Quality validation checklist with all items marked as completed

The spec follows the template structure and addresses all requirements from the user description, including the dark robotics-oriented theme, typography requirements, and all section layouts.

## Outcome

- ✅ Impact: Created complete specification for landing page UI upgrade with quality validation
- 🧪 Tests: Spec validated against 15-point quality checklist
- 📁 Files: Created spec.md and requirements checklist in specs/004-upgrade-landing-ui/
- 🔁 Next prompts: Ready for planning phase with `/sp.plan`
- 🧠 Reflection: Specification successfully captures all requirements from user description with clear, testable requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All quality checklist items validated
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase