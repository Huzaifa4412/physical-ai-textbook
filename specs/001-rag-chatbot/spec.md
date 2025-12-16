# Feature Specification: Physical AI RAG Chatbot

**Feature Branch**: `001-rag-chatbot`
**Created**: 2025-12-08
**Status**: Draft
**Input**: User description: "Create "physical-ai-rag-chatbot" feature for existing Physical AI book per Constitution v1.1.0: 1) Ingest ALL /docs/*.mdx (ROS2, Gazebo, Isaac Sim, VLA modules) via folder scan, chunk by h2/h3+paragraphs+code blocks (512 tokens, 20% overlap). 2) Embed to Qdrant 'physical-ai-corpus' using text-embedding-3-small via Gemini client. 3) FastAPI Agent('BookRAG') w/ OpenAI Agents SDK: model=gemini-2.0-flash-exp (AsyncOpenAI base_url='https://generativelanguage.googleapis.com/v1beta/openai/', GEMINI_API_KEY), retrieval_tool=qdrant_search(top_k=5, score>0.7). 4) Instructions: "Answer using ONLY retrieved book context. Cite [file:line]. 50% citations must reference peer-reviewed sources per Principle 4. If not in book: 'Not covered in Physical AI textbook.'" 5) Chainlit UI at /chat. 6) docker-compose.yml. 7) GitHub Actions re-ingest on /docs/ changes. "

## Clarifications

### Session 2025-12-08
- Q: How should the RAG chatbot handle user session data and chat history? → A: Preserve MDX frontmatter/admonitions/Mermaid as chunk metadata. Code blocks: separate chunks, retain language syntax. Handle citations: extract APA refs for RAG filtering. Multi-turn: session storage 10 messages max. Error handling: Qdrant down→fallback to keyword search /docs/. Test queries: "ROS2 rclpy publisher example", "Isaac Sim USD assets".
- Q: What is the estimated total number of .mdx documents and their average size that the system should be designed to handle initially? → A: Small Scale (<100 docs).
- Q: What level of observability is required for the RAG chatbot? → A: Minimal.
- Q: What are the expectations for the system's scalability beyond the initial small scale? → A: Designed for future scalability.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question and Get a Book-Grounded Answer (Priority: P1)

As a reader of the Physical AI textbook, I want to ask a question in a chat interface and receive an answer that is directly based on the book's content, so that I can quickly clarify concepts and find information without manually searching the documentation.

**Why this priority**: This is the core functionality of the RAG chatbot and provides the primary value to the user.

**Independent Test**: Can be tested by asking a question that is known to be in the book and verifying that the answer is accurate, cites the correct source, and is delivered through the chat UI.

**Acceptance Scenarios**:

1.  **Given** the RAG chatbot is running and has ingested the book content, **When** a user asks a question like "What is ROS 2?" in the `/chat` UI, **Then** the system provides a concise and accurate answer based on the content of `/docs/001-ros2-nervous-system/01-introduction-to-ros2.md` and cites the source file and line number.
2.  **Given** the chatbot is asked a question, **When** the retrieved context does not contain the answer, **Then** the chatbot responds with "This topic is not covered in the Physical AI textbook."
3.  **Given** the RAG chatbot is running, **When** a user asks "What is an example of an rclpy publisher?", **Then** the system returns a relevant code block and explanation from the book.
4.  **Given** the RAG chatbot is running, **When** a user asks "Where can I find USD assets for Isaac Sim?", **Then** the system provides relevant information on locating or creating USD assets.
5.  **Given** the Qdrant service is unavailable, **When** a user asks a question, **Then** the system falls back to a keyword search of the `/docs/` directory and provides a best-effort answer based on that search.


### User Story 2 - Automated Content Ingestion (Priority: P2)

As a project maintainer, I want the RAG system to automatically update its knowledge base whenever the book's documentation (`/docs/*.mdx`) changes, so that the chatbot always provides answers based on the latest content.

**Why this priority**: This ensures the long-term accuracy and relevance of the chatbot, but it is secondary to the core user-facing query functionality.

**Independent Test**: Can be tested by pushing a change to a `.mdx` file in the `/docs/` directory and verifying that a GitHub Action is triggered, which successfully re-ingests the content. A subsequent query that depends on the new content should return an updated answer.

**Acceptance Scenarios**:

1.  **Given** a developer merges a pull request that modifies a file in the `/docs/` directory, **When** the changes are pushed to the main branch, **Then** a GitHub Actions workflow is triggered to re-run the ingestion and embedding process.
2.  **Given** the content of a `.mdx` file has been updated and re-ingested, **When** a user asks a question related to the updated content, **Then** the chatbot provides an answer reflecting the new information.

### Edge Cases

-   What happens when the user asks a question that is ambiguous or has multiple possible interpretations?
-   How does the system handle questions in languages other than English?
-   How does the system handle very long questions or conversations that approach the token limit?
-   What happens if the fallback keyword search returns no results?
-   How are failures in the GitHub Actions ingestion process reported?

## Interaction and UX Flow

- **Multi-Turn Conversations**: The system MUST maintain conversational context for up to a maximum of 10 messages (user queries + bot responses). This context will be stored in session storage on the client-side and passed with each request.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST scan and ingest all `.mdx` files from the `/docs/` directory.
-   **FR-002**: The system MUST chunk the ingested content with a maximum chunk size of 512 tokens and 20% overlap. The chunking strategy MUST treat code blocks as separate chunks and preserve MDX frontmatter, admonitions, and Mermaid diagrams as metadata associated with their respective chunks.
-   **FR-003**: The system MUST generate embeddings for each chunk using the `text-embedding-3-small` model.
-   **FR-004**: The system MUST store the embeddings and their associated metadata (including source file, line numbers, language for code blocks, frontmatter, etc.) in a Qdrant vector database collection named `physical-ai-corpus`.
-   **FR-005**: The system MUST provide a FastAPI-based agent named `BookRAG`.
-   **FR-006**: The agent MUST use the `gemini-2.0-flash-exp` model for generating answers.
-   **FR-007**: The agent MUST retrieve the top 5 most relevant document chunks from Qdrant, provided their similarity score is greater than 0.7.
-   **FR-008**: The agent MUST answer questions using only the retrieved book context.
-   **FR-009**: The agent MUST cite the source file and line number for the information used in the answer (e.g., `[docs/path/to/file.mdx:10-25]`).
-   **FR-010**: If the answer cannot be found in the retrieved context, the agent MUST respond with the exact phrase: "This topic is not covered in the Physical AI textbook."
-   **FR-011**: The system MUST provide a web-based chat interface at the `/chat` endpoint using Chainlit.
-   **FR-012**: The entire application MUST be deployable via a single `docker-compose.yml` file.
-   **FR-013**: A GitHub Actions workflow MUST be configured to automatically trigger the content ingestion and embedding process upon any changes to files in the `/docs/` directory on the main branch.
-   **FR-014**: The system MUST extract APA-style references from the text and store them as metadata to be used for filtering during retrieval.
-   **FR-015**: In the event that the Qdrant service is unavailable, the system MUST gracefully degrade to a keyword-based search against the raw `.mdx` files in the `/docs/` directory.
-   **FR-016**: The system MUST be optimized to handle a small scale of content initially (<100 `.mdx` documents).
-   **FR-017**: The system MUST implement basic logging for errors and key events.
-   **FR-018**: The system architecture MUST allow for future horizontal scaling of components (e.g., Qdrant, FastAPI agent) without implementing complex scaling solutions upfront.

### Key Entities *(include if feature involves data)*

-   **Document Chunk**: A portion of text and/or code extracted from a source `.mdx` file. It has content and metadata (source file, line numbers, language, frontmatter, admonitions, Mermaid diagrams, parsed APA citations).
-   **Embedding**: A vector representation of a Document Chunk.
-   **Chat Session**: A sequence of up to 10 user questions and chatbot answers stored in the client's session storage.

## Constitution Alignment *(mandatory)*

-   **Principle 1: Accuracy and Verifiability**: This spec adheres to this principle by requiring answers to be grounded *only* in the book's content and by mandating citations.
-   **Principle 3: Reproducibility and Automation**: The use of `docker-compose.yml` for deployment and GitHub Actions for automated ingestion ensures reproducibility.
-   **Principle 4: Architectural Rigor**: The spec defines the core components (FastAPI, Qdrant, Chainlit) and their interactions.
-   **Principle 5: Retrieval Fidelity**: This spec is written to be in full compliance with Principle 5, detailing the data source, chunking strategy, embedding model, vector store, generation model, and retrieval thresholds as defined in the constitution. The requirement for 50% of citations to reference peer-reviewed sources from the book content will be enforced by the agent's prompt instructions and the extraction of APA references.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 95% of answers to questions directly covered in the book MUST be factually accurate when compared against the source `.mdx` files.
-   **SC-002**: For 100% of generated answers that are not a "not covered" response, a valid and correct source file and line number citation MUST be provided.
-   **SC-003**: The system MUST produce zero hallucinations (i.e., fabricated facts or sources not present in the book).
-   **SC-004**: The end-to-end response time for a user query (from question submission to answer displayed in the UI) SHOULD be less than 5 seconds for 90% of queries.