# Data Model: Physical AI RAG Chatbot

## Core Entities

### DocumentChunk
**Description**: A portion of text and/or code extracted from a source `.mdx` file with associated metadata.

**Fields**:
- `id` (str): Unique identifier for the chunk
- `content` (str): The actual text content of the chunk (max 512 tokens)
- `source_file` (str): Path to the original .mdx file
- `start_line` (int): Starting line number in the source file
- `end_line` (int): Ending line number in the source file
- `language` (str, optional): Programming language for code blocks
- `metadata` (dict): Additional metadata (frontmatter, admonitions, Mermaid diagrams)
- `embedding` (list[float]): Vector embedding of the content
- `created_at` (datetime): Timestamp when chunk was created
- `updated_at` (datetime): Timestamp when chunk was last updated

**Relationships**:
- Belongs to one source Document
- Used in multiple Retrieval operations

### Document
**Description**: Represents a single .mdx file from the /docs/ directory.

**Fields**:
- `id` (str): Unique identifier for the document
- `file_path` (str): Path to the .mdx file
- `title` (str): Title from frontmatter or first heading
- `last_modified` (datetime): Last modification time of the file
- `size` (int): Size of the document in bytes
- `checksum` (str): SHA256 hash for change detection
- `created_at` (datetime): Timestamp when document was first processed
- `updated_at` (datetime): Timestamp when document was last processed

**Relationships**:
- Has many DocumentChunks
- Associated with many Citations

### ChatSession
**Description**: A conversation session containing up to 10 user questions and chatbot responses.

**Fields**:
- `session_id` (str): Unique identifier for the session
- `messages` (list[dict]): List of messages (user queries and bot responses)
- `created_at` (datetime): Timestamp when session was created
- `last_accessed` (datetime): Timestamp of last interaction
- `metadata` (dict): Additional session metadata

**Message Structure**:
- `role` (str): Either "user" or "assistant"
- `content` (str): The message content
- `timestamp` (datetime): When the message was created
- `citations` (list[str], optional): Citations for assistant responses

### Citation
**Description**: Reference to a specific location in a document used in an answer.

**Fields**:
- `id` (str): Unique identifier for the citation
- `document_chunk_id` (str): Reference to the source chunk
- `source_file` (str): Path to the original file
- `line_range` (tuple[int, int]): Start and end line numbers
- `text_snippet` (str): Brief excerpt from the cited text
- `confidence_score` (float): Similarity score from retrieval

**Relationships**:
- References one DocumentChunk
- Associated with one ChatSession message

### APAReference
**Description**: Academic reference extracted from the documentation for citation filtering.

**Fields**:
- `id` (str): Unique identifier for the reference
- `citation_text` (str): Full APA-formatted citation
- `authors` (list[str]): List of authors
- `title` (str): Title of the work
- `journal` (str): Journal or publication name
- `year` (int): Publication year
- `doi` (str, optional): Digital Object Identifier
- `source_document` (str): Document where reference was found
- `extracted_at` (datetime): When reference was extracted

**Relationships**:
- Associated with one or more DocumentChunks that reference it

## Qdrant Collection Schema

### physical-ai-corpus
**Description**: Main collection for storing document chunks with embeddings.

**Payload Fields**:
- `content` (str): The chunk content
- `source_file` (str): Path to source file
- `start_line` (int): Starting line number
- `end_line` (int): Ending line number
- `language` (str, optional): Programming language for code chunks
- `metadata` (dict): Additional document metadata
- `apa_references` (list[str]): Extracted APA references in this chunk
- `frontmatter` (dict): Original MDX frontmatter
- `checksum` (str): Content checksum for change detection

**Vector Configuration**:
- Size: Determined by embedding model (text-embedding-3-small)
- Distance: Cosine similarity

## Session Storage Schema

### Client-Side Session Data
**Structure**:
```json
{
  "sessionId": "unique-session-identifier",
  "messages": [
    {
      "id": "message-uuid",
      "role": "user|assistant",
      "content": "message text",
      "timestamp": "ISO 8601 datetime",
      "citations": [
        {
          "file": "path/to/source.mdx",
          "lines": [start, end],
          "text": "brief snippet"
        }
      ]
    }
  ],
  "createdAt": "ISO 8601 datetime",
  "lastInteraction": "ISO 8601 datetime"
}
```

## Validation Rules

### DocumentChunk Validation
- Content must be ≤ 512 tokens
- Source file must exist in /docs/ directory
- Line numbers must be valid within the source file
- Embedding vector must have correct dimensions

### ChatSession Validation
- Must not exceed 10 messages in total
- Messages must alternate between user and assistant
- Session ID must be unique
- Timestamps must be in chronological order

### Citation Validation
- Confidence score must be > 0.7 to be valid
- Line range must be valid within the source document
- Citation must reference actual content in the document

## State Transitions

### Document States
- `PENDING` → `PROCESSING` → `EMBEDDED` → `INDEXED` → `AVAILABLE`
- `AVAILABLE` → `CHANGED` → `PROCESSING` (when source file is modified)

### ChatSession States
- `ACTIVE` (when within 10-message limit)
- `LIMIT_REACHED` (when 10 messages reached)
- `EXPIRED` (after inactivity period)