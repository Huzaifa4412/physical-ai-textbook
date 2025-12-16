---
id: 1
title: Create specification for RAG chatbot
stage: spec
date: 2025-12-08
surface: agent
model: Gemini
feature: 001-rag-chatbot
branch: 001-rag-chatbot
user: {{USER}}
command: /sp.specify "Create "physical-ai-rag-chatbot" feature for existing Physical AI book per Constitution v1.1.0: 1) Ingest ALL /docs/*.mdx (ROS2, Gazebo, Isaac Sim, VLA modules) via folder scan, chunk by h2/h3+paragraphs+code blocks (512 tokens, 20% overlap). 2) Embed to Qdrant 'physical-ai-corpus' using text-embedding-3-small via Gemini client. 3) FastAPI Agent('BookRAG') w/ OpenAI Agents SDK: model=gemini-2.0-flash-exp (AsyncOpenAI base_url='https://generativelanguage.googleapis.com/v1beta/openai/', GEMINI_API_KEY), retrieval_tool=qdrant_search(top_k=5, score>0.7). 4) Instructions: "Answer using ONLY retrieved book context. Cite [file:line]. 50% citations must reference peer-reviewed sources per Principle 4. If not in book: 'Not covered in Physical AI textbook.'" 5) Chainlit UI at /chat. 6) docker-compose.yml. 7) GitHub Actions re-ingest on /docs/ changes. "
labels: ["spec", "rag", "chatbot"]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-chatbot/spec.md
  - specs/001-rag-chatbot/checklists/requirements.md
tests:
null
---

## Prompt

Create "physical-ai-rag-chatbot" feature for existing Physical AI book per Constitution v1.1.0: 1) Ingest ALL /docs/*.mdx (ROS2, Gazebo, Isaac Sim, VLA modules) via folder scan, chunk by h2/h3+paragraphs+code blocks (512 tokens, 20% overlap). 2) Embed to Qdrant 'physical-ai-corpus' using text-embedding-3-small via Gemini client. 3) FastAPI Agent('BookRAG') w/ OpenAI Agents SDK: model=gemini-2.0-flash-exp (AsyncOpenAI base_url='https://generativelanguage.googleapis.com/v1beta/openai/', GEMINI_API_KEY), retrieval_tool=qdrant_search(top_k=5, score>0.7). 4) Instructions: "Answer using ONLY retrieved book context. Cite [file:line]. 50% citations must reference peer-reviewed sources per Principle 4. If not in book: 'Not covered in Physical AI textbook.'" 5) Chainlit UI at /chat. 6) docker-compose.yml. 7) GitHub Actions re-ingest on /docs/ changes. 

## Response snapshot

I have created the feature specification for the RAG chatbot.
The specification is located at: `specs/001-rag-chatbot/spec.md`
A checklist to validate the specification has been created at: `specs/001-rag-chatbot/checklists/requirements.md`
The feature branch is `001-rag-chatbot`.

## Outcome

- ✅ Impact: Created a detailed specification for the RAG chatbot feature, including user stories, functional requirements, and success criteria.
- 🧪 Tests: No tests were run.
- 📁 Files: Created 2 new files: the spec and the requirements checklist.
- 🔁 Next prompts: The specification is ready for the planning phase (`/sp.plan`).
- 🧠 Reflection: The script for creating a new feature failed, so I had to manually perform the steps. This should be investigated to make the process smoother in the future.

## Evaluation notes (flywheel)

- Failure modes observed: The PowerShell script for creating a new feature failed due to a parameter binding issue.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Investigate the PowerShell script to understand why it fails with long string arguments.
