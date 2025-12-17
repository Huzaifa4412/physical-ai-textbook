---
id: 001
title: "Physical AI UI Spec"
stage: spec
date: "2025-12-17"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "physical-ai-ui"
branch: "003-physical-ai-ui"
user: "user"
command: "/sp.specify"
labels: ["ui-design", "specification", "physical-ai"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/003-physical-ai-ui/spec.md"
  - "specs/003-physical-ai-ui/checklists/requirements.md"
tests: []
outcome: "Successfully created specification for Physical AI & Humanoid UI"
evaluation: "Specification meets all requirements with clear user stories, functional requirements, and success criteria"
---

## PROMPT_TEXT

# /sp.specify — Physical AI & Humanoids (Short)

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

"Physical AI & Humanoid Systems"

Subtitle (1–2 lines, technical tone):

"A deep, engineering-focused guide to embodied intelligence, humanoid robots, perception, control, and real-world AI systems."

Supporting line (optional):

"From sensors and simulation to autonomy and deployment."

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

**End**

## RESPONSE_TEXT

Successfully created the specification for the Physical AI & Humanoid UI feature. The specification includes:

1. User Scenarios & Testing with 4 prioritized user stories covering professional book introduction, technical content discovery, research assistant access, and professional visual design
2. Functional Requirements (FR-001 to FR-015) detailing all necessary system capabilities
3. Key Entities including Homepage Content, Chat Assistant Interface, and Visual Design System
4. Constitution Alignment with relevant principles
5. Success Criteria with measurable outcomes (SC-001 to SC-005)

The specification was validated against quality criteria and a checklist was created at specs/003-physical-ai-ui/checklists/requirements.md. The feature branch 003-physical-ai-ui has been created and the spec file is ready for the next phase.