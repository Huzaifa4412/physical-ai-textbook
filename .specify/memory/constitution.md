<!--
[SYNC_IMPACT_REPORT_START]
Version change: 1.1.0 -> 1.2.0
Modified principles:
  - Principle 1: Accuracy and Verifiability (updated Rule 1.1 to remove Context7)
Added sections:
  - Principle 5: Retrieval Fidelity
Removed sections: None
Templates requiring updates:
  - [ ] .specify/templates/spec-template.md
  - [ ] .specify/templates/plan-template.md
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Set the initial ratification date of the constitution.
[SYNC_IMPACT_REPORT_END]
-->
# Physical AI Textbook Constitution

| Version | Ratification Date | Last Amended | Status |
|---|---|---|---|
| 1.2.0 | [RATIFICATION_DATE] | 2025-12-08 | Active |

## I. Preamble

This constitution establishes the foundational principles, architectural standards, and operational mandates governing the **Physical AI Textbook**. Its purpose is to ensure all development artifacts—from specifications to code—are accurate, clear, reproducible, and rigorously engineered. Adherence to this document is mandatory for all contributors and automated agents.

## II. Core Principles

### Principle 1: Accuracy and Verifiability

**Core Rule:** Every statement, code snippet, and architectural decision MUST be grounded in verifiable, up-to-date sources. Claims about system behavior MUST be backed by executable tests or references to authoritative documentation.

- **1.1 Source Priority:** Authoritative sources include official documentation, peer-reviewed papers, or stable source code.
- **1.2 Fact-Checking:** Automated information retrieval (e.g., RAG) MUST be aggressively fact-checked against trusted sources. Unverified or ambiguous information MUST be flagged.
- **1.3 Test-Driven Claims:** Any assertion about code behavior (e.g., "this function is idempotent") MUST be accompanied by a test case that proves it.

**Rationale:** The project's credibility depends on the complete accuracy of its content. This principle prevents the propagation of misinformation, outdated practices, and "hallucinated" facts from AI agents.

### Principle 2: Clarity and Plain Language

**Core Rule:** All generated text, from user-facing documentation to internal specifications, MUST be clear, concise, and accessible to a target audience with a moderate technical background.

- **2.1 Simplicity Over Jargon:** Avoid esoteric jargon. If a complex term is necessary, it MUST be defined in a glossary or at its first use. All outputs MUST be suitable for a professional setting.
- **2.2 Structured Content:** Use headings, lists, and tables to structure information logically. Long paragraphs are discouraged.
- **2.3 Action-Oriented Language:** Instructions and tasks MUST be phrased as clear, actionable commands (e.g., "Run the `setup.sh` script," not "You might want to run the script").

**Rationale:** Clarity reduces ambiguity, minimizes the risk of misinterpretation, and makes the project's outputs immediately useful to a broader audience.

### Principle 3: Reproducibility and Automation

**Core Rule:** Every process, from setting up a development environment to running a final build, MUST be automated and reproducible. "It works on my machine" is not an acceptable state.

- **3.1 Scripted Everything:** All setup, testing, and deployment procedures MUST be codified in scripts (e.g., shell, PowerShell, Dockerfile).
- **3.2 Idempotent Operations:** Scripts and automated processes MUST be idempotent. Running a process multiple times should not produce errors or unintended side effects.
- **3.3 Pinned Dependencies:** All external dependencies (libraries, tools, base images) MUST be pinned to specific, known-good versions.

**Rationale:** Automation guarantees consistency, eliminates manual error, and enables reliable, repeatable outcomes for all users and contributors.

### Principle 4: Architectural Rigor

**Core Rule:** The system's architecture MUST be explicitly defined, consistently applied, and resilient to change. "Ad-hoc" or unplanned architectural changes are forbidden.

- **4.1 Spec-Driven Development:** All feature work MUST begin with a formal specification (`spec.md`) that defines scope, interfaces, and non-functional requirements. No code is written before a spec is approved.
- **4.2 Modular and Decoupled:** The system MUST be composed of modular, loosely-coupled components with well-defined interfaces. This is tracked in `plan.md` and enforced via code reviews and ADRs.
- **4.3 Traceability:** Every line of code MUST be traceable back to a specific task (`tasks.md`) and requirement (`spec.md`). Commits MUST reference the associated task ID.

**Rationale:** A rigorous architectural process ensures the system is maintainable, scalable, and easy to reason about over the long term.

### Principle 5: Retrieval Fidelity

**Core Rule:** The Retrieval-Augmented Generation (RAG) system MUST adhere to strict rules for sourcing, processing, and generating content to ensure relevance and accuracy.

- **5.1 Authoritative Corpus:** The RAG system MUST retrieve information *only* from Markdown (`.mdx`) files located within the `/docs/` directory of the project repository.
- **5.2 Data Processing:** Content MUST be chunked at a maximum of 512 tokens. The chunking process MUST preserve the integrity of code blocks and YAML frontmatter.
- **5.3 Vectorization and Storage:** Document chunks MUST be vectorized using the `text-embedding-3-small` model and.
- **5.4 Generation Model:** The generative model for synthesizing answers MUST be Gemini, accessed via an `AsyncOpenAI` compatible client with the base URL `https://generativelanguage.googleapis.com/v1beta/openai/`.
- **5.5 Citation Requirement:** At least 50% of all generated responses that rely on retrieved context MUST cite peer-reviewed sources referenced within the book's content.
- **5.6 Operational Constraints:**
    - The implementation MUST operate within the Free Gemini tier, respecting a limit of 15 Requests Per Minute (RPM).
    - Multi-turn conversational context MUST NOT exceed 5,000 tokens.
    - Retrieved document chunks MUST have a similarity score greater than 0.7 to be considered for generation.
- **5.7 Success Metrics:**
    - The system MUST achieve at least 95% accuracy in its answers when evaluated against the source book content.
    - The system MUST produce zero hallucinations (i.e., fabricated facts or sources).

**Rationale:** This principle establishes a tight operational envelope for the RAG chatbot to ensure its outputs are trustworthy, directly traceable to the project's knowledge base, and operate within defined technical and resource constraints.

## III. Governance and Amendment

### 1. Versioning

This constitution follows a semantic versioning scheme:
- **MAJOR (X.y.z):** Reserved for backward-incompatible changes, such as removing a core principle.
- **MINOR (x.Y.z):** For adding new principles or significant, backward-compatible expansions of existing ones.
- **PATCH (x.y.Z):** For clarifications, typo fixes, and non-substantive changes.

### 2. Amendment Process

Amendments can be proposed via a pull request against this file. The proposal MUST include:
- A clear rationale for the change.
- An updated version number in accordance with the versioning policy.
- A review and explicit approval from at least two project maintainers.

### 3. Compliance

All automated agents and human contributors are bound by the principles herein. Code or documentation that violates this constitution will be rejected during review. Regular audits will be conducted to ensure ongoing.