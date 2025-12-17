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