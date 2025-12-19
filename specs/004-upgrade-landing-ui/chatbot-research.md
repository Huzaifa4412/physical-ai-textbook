# Research: Chatbot API Integration Issue

## Problem Statement
The chatbot is not working properly despite the API being correct when tested in Postman. The frontend chatbot components fail to communicate with the backend API.

## Root Cause Analysis

### 1. API Contract Mismatch
- **Backend Expectation** (Backend/agent.py lines 90-96):
  ```python
  class ChatRequest(BaseModel):
      question: str
  ```
  The deployed API expects a JSON payload with a `question` field and responds with an `answer` field.

- **Frontend Implementation** (site/src/theme/ChatWidget.js lines 54-57):
  ```javascript
  body: JSON.stringify({
    query: message,
    conversation_id: conversationId
  })
  ```
  The frontend is sending `query` and `conversation_id` fields instead of `question`.

- **Alternative Frontend** (site/src/components/ChatbotWidget/ChatbotWidget.js lines 31-37):
  ```javascript
  body: JSON.stringify({
    message: userMessage.text,
    metadata: {
      userType: 'engineer',
      context: 'physical-ai-book'
    }
  }),
  ```
  This implementation also sends the wrong field names.

### 2. Response Handling Issue
The backend responds with an `answer` field, but the frontend expects different response formats:
- `site/src/theme/ChatWidget.js` expects `data.response` (line 71)
- `site/src/components/ChatbotWidget/ChatbotWidget.js` expects `data.response` (line 48)

### 3. Recent Changes
The recent commit `ff9289e` updated the chatbot backend hosting path from local endpoints (`/api/chat`, `/api/chat/send`) to the deployed endpoint (`https://api-deployment-vercel-tau.vercel.app/chat`), but the request/response format was not updated accordingly.

### 4. Postman vs Frontend Difference
Postman likely works because the user is manually sending the correct payload format: `{question: "user query"}` and receiving `{answer: "response"}`, while the frontend is sending the old/incorrect format.

## Decision: Update Frontend Request and Response Format
The frontend implementations must be updated to send the correct request format and handle the correct response format expected by the deployed backend API.

## Rationale
The deployed backend API contract is fixed and working (as verified by Postman). The issue is that the frontend is not sending the expected payload format and not handling the response correctly. Updating the frontend to match the backend contract is the minimal change required to fix the issue.

## Alternatives Considered
1. Change the backend API to accept multiple formats - Not feasible as the backend is already deployed
2. Deploy a new backend to match frontend format - Would require additional deployment and potentially break other clients
3. Update frontend to match existing backend - Simplest and most appropriate solution

## Implementation Plan
Update both frontend components to send the correct request format and handle the response correctly:
- Change `query` field to `question`
- Change `message` field to `question`
- Update response handling to use `data.answer` instead of `data.response`
- Remove unnecessary fields like `conversation_id` and `metadata` that the backend doesn't expect