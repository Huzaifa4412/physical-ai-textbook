# Data Model: Upgrade Landing Page UI

## UI Components

### Landing Page Content
- **name**: Landing Page Content
- **description**: Represents the visual elements and information displayed on the landing page, including hero text, feature descriptions, and navigation elements
- **fields**:
  - title: string (e.g., "Physical AI & Humanoid Systems")
  - subtitle: string (e.g., "embodied intelligence, robotics, real-world AI")
  - supportingText: string (e.g., "robot brains → deployment")
  - primaryCtaText: string (e.g., "Start Reading")
  - primaryCtaUrl: string (e.g., "/docs/category/introduction")
  - secondaryCtaText: string (e.g., "View Structure")
  - secondaryCtaUrl: string (e.g., "/docs/category/introduction")
  - featureCards: array of FeatureCard objects
  - bentoGridItems: array of BentoGridItem objects
  - learningPathItems: array of LearningPathItem objects

### FeatureCard
- **name**: FeatureCard
- **description**: Represents a feature highlight card in the landing page features section
- **fields**:
  - title: string (e.g., "Physical AI First")
  - description: string (e.g., "Intelligence grounded in physics and embodiment")
  - icon: string (optional, icon identifier)

### BentoGridItem
- **name**: BentoGridItem
- **description**: Represents an item in the bento grid layout for core topics
- **fields**:
  - title: string (e.g., "Robot Brain Architecture")
  - description: string (optional, short description)
  - icon: string (optional, icon identifier)

### LearningPathItem
- **name**: LearningPathItem
- **description**: Represents an item in the learning path sequence
- **fields**:
  - title: string (e.g., "Foundations")
  - description: string (optional, short description of the topic)

### NavigationItem
- **name**: NavigationItem
- **description**: Represents a navigation link in the navbar or footer
- **fields**:
  - label: string (e.g., "Docs", "GitHub")
  - url: string (e.g., "/docs", "https://github.com/...")
  - position: string (e.g., "left", "right" for navbar placement)

## Validation Rules

### Landing Page Content
- title must be 1-100 characters
- subtitle must be 1-200 characters
- primaryCtaText must be 1-50 characters
- primaryCtaUrl must be a valid relative or absolute URL
- secondaryCtaText must be 1-50 characters
- secondaryCtaUrl must be a valid relative or absolute URL
- featureCards array must contain 3-4 items

### FeatureCard
- title must be 1-50 characters
- description must be 1-200 characters

### BentoGridItem
- title must be 1-50 characters
- description must be 0-200 characters

### LearningPathItem
- title must be 1-50 characters
- description must be 0-200 characters

### NavigationItem
- label must be 1-50 characters
- url must be a valid relative or absolute URL

## State Transitions

The landing page content is static and doesn't have state transitions. The UI components will have visual states for:
- Default state
- Hover state (for interactive elements)
- Focus state (for accessibility)
- Loading state (if applicable)
- Responsive states (desktop, tablet, mobile)

## Chatbot Data Models

### ChatMessage
Represents a message in the chat conversation

**Fields:**
- `id`: string/number - Unique identifier for the message
- `message`: string - The text content of the message
- `sender`: string - Either "user" or "assistant"
- `timestamp`: Date - When the message was created

**State Transitions:**
- Created when user sends a message
- Updated when assistant responds

### ChatRequest
Represents the request sent to the backend API

**Fields:**
- `question`: string - The user's question/query (required)
- `session_id`: string - Optional session identifier

**Validation:**
- `question` field is required
- `question` must not be empty

### ChatResponse
Represents the response received from the backend API

**Fields:**
- `answer`: string - The answer from the AI assistant (required)
- `session_id`: string - Session identifier (optional)

**Validation:**
- `answer` field is required
- `answer` must not be empty

## API Contracts

### Request Format
```json
{
  "question": "User's question text"
}
```

### Response Format
```json
{
  "answer": "AI's response text"
}
```

## Relationships

- One ChatMessage belongs to one ChatSession
- One ChatSession contains multiple ChatMessages
- ChatRequest and ChatResponse are part of the API communication cycle