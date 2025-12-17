# Quickstart: Upgrade Landing Page UI

## Prerequisites

- Node.js >= 20.0
- npm or yarn package manager
- Git for version control

## Setup Development Environment

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd physical-ai-textbook
   ```

2. **Navigate to the site directory**:
   ```bash
   cd site
   ```

3. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Start the development server**:
   ```bash
   npm start
   # or
   yarn start
   ```

   This will start the Docusaurus development server at http://localhost:3000

## Implementation Steps

### 1. Update the Landing Page Structure

1. **Modify `site/src/pages/index.tsx`** to implement the new layout with:
   - Updated Navbar with sticky positioning
   - Hero section with specified content
   - Feature cards section (4 cards as specified)
   - Bento grid section for core topics
   - Learning path section
   - "Who This Book Is For" section
   - Updated footer

2. **Update CSS modules** in `site/src/pages/index.module.css`:
   - Implement the dark robotics-oriented theme
   - Apply proper typography (system-ui, headings 600-700, body 400)
   - Set max line width to ~70ch
   - Use borders over shadows for visual separation

### 2. Create New Components

1. **Feature Cards Component** (`site/src/components/HomepageFeatures/index.tsx`):
   - Create 4 feature cards with specified content
   - Apply surface background with subtle borders
   - Ensure equal height and clean grid layout

2. **Bento Grid Component** (`site/src/components/LandingSections/BentoGrid.tsx`):
   - Implement asymmetric but clean bento-style grid
   - Include 6 core topics with text-first approach
   - Add optional minimal icons

3. **Learning Path Component** (`site/src/components/LandingSections/LearningPath.tsx`):
   - Create visual representation of learning progression
   - Include 6 stages: Foundations, Perception, World Modeling, Planning & Control, Autonomy, Sim-to-Real

### 3. Update Global Styles

1. **Review `site/src/css/custom.css`**:
   - Ensure color variables match specifications:
     - Background: #0b0e14
     - Surface: #111827
     - Primary text: #e5e7eb
     - Secondary text: #9ca3af
     - Borders: #1f2937
     - Accent: #3b82f6
     - Accent hover: #2563eb

2. **Create new CSS modules**:
   - `site/src/css/buttons.module.css` for button styles
   - `site/src/css/cards.module.css` for card styles

### 4. Update Navigation

1. **Modify Navbar** in Docusaurus config or custom theme:
   - Left: Site/Book title
   - Right: Docs, Book Structure, GitHub links
   - Sticky but minimal height
   - Bottom border only

2. **Update Footer**:
   - Book title and short description
   - Links: Docs, GitHub, License/About
   - Top border only

## Testing

1. **Visual Testing**:
   - Verify all sections appear as specified
   - Check color theme implementation
   - Confirm typography settings
   - Test responsive design on different screen sizes

2. **Accessibility Testing**:
   - Verify WCAG 2.1 AA compliance
   - Test keyboard navigation
   - Check screen reader compatibility
   - Validate color contrast ratios

3. **Performance Testing**:
   - Ensure page loads under 2 seconds
   - Test with reduced motion preferences
   - Verify smooth interactions

## Build and Deployment

1. **Build the site**:
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Preview the build locally**:
   ```bash
   npm run serve
   # or
   yarn serve
   ```

## Common Issues and Solutions

- **CSS Modules not applying styles**: Ensure class names are properly exported and imported
- **Docusaurus components not rendering**: Verify component exports and import paths
- **Color variables not working**: Check that custom.css is properly imported in the Docusaurus config
- **Responsive layout issues**: Test on multiple screen sizes and adjust CSS media queries as needed