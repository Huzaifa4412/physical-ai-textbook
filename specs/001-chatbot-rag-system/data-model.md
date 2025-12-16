# Data Model: Chatbot System for Physical AI Textbook

## Entities

### 1. ConversationSession
**Description**: Represents a single conversation session between user and chatbot

**Fields**:
- id: string (unique identifier)
- userId: string (user identifier, anonymous if not logged in)
- createdAt: timestamp (session start time)
- updatedAt: timestamp (last activity time)
- isActive: boolean (whether session is currently active)
- metadata: object (additional session data)

**Relationships**:
- Contains multiple Message entities
- Links to User (if authenticated)

### 2. Message
**Description**: Represents a single message in a conversation

**Fields**:
- id: string (unique identifier)
- conversationId: string (reference to parent conversation)
- sender: enum ('user' | 'assistant')
- content: string (message text content)
- timestamp: timestamp (when message was sent)
- metadata: object (additional message data like citations)

**Relationships**:
- Belongs to ConversationSession
- May reference ContentChunk for source citations

### 3. ContentChunk
**Description**: Represents a chunk of textbook content stored in vector database

**Fields**:
- id: string (unique identifier)
- sourceUrl: string (URL of original content)
- content: string (text content of the chunk)
- embedding: array<number> (vector embedding of the content)
- title: string (title of the source page)
- metadata: object (additional content metadata like section, tags)

**Relationships**:
- May be referenced by multiple Message entities as source citations

### 4. UserQuery
**Description**: Represents a user query and its processing information

**Fields**:
- id: string (unique identifier)
- conversationId: string (reference to conversation)
- originalQuery: string (user's original query)
- processedQuery: string (query after processing)
- timestamp: timestamp (when query was made)
- relevantChunks: array<ContentChunk> (chunks retrieved for response)
- responseId: string (reference to generated response)

**Relationships**:
- Belongs to ConversationSession
- References multiple ContentChunk entities
- Links to Message (response)

### 5. EmbeddingModel
**Description**: Represents the embedding model used for content processing

**Fields**:
- id: string (unique identifier)
- name: string (model name)
- dimension: number (embedding vector dimension)
- provider: string (model provider)
- version: string (model version)
- createdAt: timestamp

**Relationships**:
- Used by multiple ContentChunk entities

### 6. APIUsage
**Description**: Tracks API usage for cost and rate limit management

**Fields**:
- id: string (unique identifier)
- userId: string (user identifier)
- service: enum ('gemini' | 'qdrant' | 'other')
- endpoint: string (API endpoint called)
- timestamp: timestamp
- tokensIn: number (input tokens)
- tokensOut: number (output tokens)
- cost: number (estimated cost)

**Relationships**:
- Links to User (if authenticated)

## State Transitions

### ConversationSession States:
- `created` → `active` (when first message is sent)
- `active` → `inactive` (after period of inactivity)
- `inactive` → `archived` (after extended inactivity or user action)

### Message States:
- `draft` → `sent` (when message is successfully sent)
- `sent` → `delivered` (when received by recipient)
- `delivered` → `read` (when viewed by recipient)

## Validation Rules

### ConversationSession:
- Must have a valid userId
- createdAt must be before updatedAt
- Cannot have more than 500 messages per session

### Message:
- Content must not exceed 10,000 characters
- Sender must be either 'user' or 'assistant'
- Must belong to an active conversation

### ContentChunk:
- Content must not be empty
- Embedding must have the correct dimension
- Source URL must be valid

### UserQuery:
- Original query must not be empty
- Must have at least one relevant chunk after processing
- Cannot be processed more than once

## Indexes

### ConversationSession:
- Index on userId for quick user session retrieval
- Index on updatedAt for session ordering
- Index on isActive for active session filtering

### Message:
- Index on conversationId for conversation retrieval
- Index on timestamp for chronological ordering
- Index on sender for message filtering

### ContentChunk:
- Index on sourceUrl for content deduplication
- Index on embedding for vector similarity search
- Index on title for text-based search