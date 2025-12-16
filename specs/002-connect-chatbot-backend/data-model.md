# Data Model: Connect Backend to Chatbot UI

## Entities

### 1. QueryRequest
**Description**: Represents a query request from the frontend UI

**Fields**:
- query: string (the user's question/query)
- conversation_id: string (optional, for maintaining conversation context)
- user_id: string (optional, for user identification)

### 2. QueryResponse
**Description**: Represents a response from the backend to the frontend UI

**Fields**:
- response: string (the AI-generated response)
- sources: array (list of source documents/references)
- conversation_id: string (ID for maintaining conversation context)
- success: boolean (whether the query was processed successfully)
- error: string (optional, error message if query failed)

### 3. SourceDocument
**Description**: Represents a source document/reference used in the response

**Fields**:
- title: string (title of the source document)
- url: string (URL of the source)
- content: string (relevant content snippet)
- score: float (relevance score from vector search)

### 4. ChatMessage
**Description**: Represents a message in a conversation

**Fields**:
- id: string (unique identifier)
- conversation_id: string (reference to parent conversation)
- sender: enum ('user' | 'assistant') (who sent the message)
- content: string (message content)
- timestamp: datetime (when the message was sent)
- sources: array (optional, sources used for assistant responses)

## Validation Rules

### QueryRequest:
- query must not be empty
- query length should be reasonable (e.g., < 1000 characters)
- conversation_id should follow proper format if provided

### QueryResponse:
- response must be provided when success is true
- sources should be properly formatted
- conversation_id should match the request if provided

### SourceDocument:
- title and url must be provided
- score should be between 0 and 1

## API Contracts

### POST /api/chat/send
**Request Body**:
```json
{
  "query": "string",
  "conversation_id": "string (optional)"
}
```

**Response**:
```json
{
  "response": "string",
  "sources": [
    {
      "title": "string",
      "url": "string",
      "content": "string",
      "score": "float"
    }
  ],
  "conversation_id": "string",
  "success": "boolean",
  "error": "string (optional)"
}
```

### GET /api/health
**Response**:
```json
{
  "status": "healthy",
  "timestamp": "string"
}
```