# Implementation Plan: Fix Chatbot API Integration

**Branch**: `004-upgrade-landing-ui` | **Date**: 2025-12-19 | **Spec**: [link]
**Input**: Feature specification from `/specs/004-upgrade-landing-ui/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix the chatbot API integration issue where the frontend is sending incorrect request format to the backend API. The backend expects a `question` field but the frontend is sending `query` or `message` fields.

## Technical Context

**Language/Version**: JavaScript/React, Python 3.11
**Primary Dependencies**: FastAPI, React, @chatscope/chat-ui-kit-react
**Storage**: N/A (API only)
**Testing**: Manual testing via UI
**Target Platform**: Web application
**Project Type**: Web application (frontend + backend API)
**Performance Goals**: <2s response time for chat queries
**Constraints**: Must maintain compatibility with deployed backend API
**Scale/Scope**: Single chatbot feature integration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All changes align with the project constitution, focusing on accuracy and verifiability. The fix addresses the API contract mismatch while maintaining architectural rigor.

## Phase 0: Research Summary

The research phase identified the root cause of the chatbot API integration issue:
1. API contract mismatch: frontend sending incorrect field names (`query`, `message`) vs backend expectation (`question`)
2. Response handling issue: frontend expecting `response` field vs backend returning `answer` field
3. Two frontend components affected: `ChatWidget.js` and `ChatbotWidget.js`

## Phase 1: Design Summary

Completed design artifacts:
- `research.md` - Root cause analysis and solution approach
- `chatbot-research.md` - Detailed chatbot-specific research
- `data-model.md` - Data models for chat messages and API contracts
- `quickstart.md` - Implementation guide for the fix
- `contracts/chatbot-api.yaml` - API contract documentation

The design ensures proper request/response format alignment between frontend and backend.

## Project Structure

### Documentation (this feature)

```text
specs/004-upgrade-landing-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── chatbot-research.md  # Chatbot-specific research
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
site/
├── src/
│   ├── theme/
│   │   └── ChatWidget.js    # Main chat widget component
│   └── components/
│       └── ChatbotWidget/
│           └── ChatbotWidget.js  # Alternative chat widget
└── src/theme/ChatWidget.css  # Chat widget styles

Backend/
├── agent.py               # Backend API implementation
└── requirements.txt       # Backend dependencies
```

**Structure Decision**: Two frontend components (ChatWidget.js and ChatbotWidget.js) need to be updated to match the backend API contract in Backend/agent.py

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [N/A] | [N/A] |
