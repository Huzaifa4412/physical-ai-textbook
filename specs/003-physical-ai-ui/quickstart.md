# Quickstart: Physical AI & Humanoid UI

## Overview
This guide provides a quick setup for the Physical AI & Humanoid UI feature development environment.

## Prerequisites
- Node.js 18+
- npm or yarn
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd physical-ai-textbook
```

### 2. Navigate to Site Directory
```bash
cd site
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Start Development Server
```bash
npm start
```

The site will be available at http://localhost:3000

## Key Files to Modify

### Homepage UI
- `src/pages/index.tsx` - Main homepage component
- `src/pages/index.module.css` - Homepage styling

### Chatbot UI
- `src/theme/ChatWidget.js` - Chat widget component
- `src/theme/ChatWidget.css` - Chat widget styling
- `src/theme/Root.js` - Global mount for chatbot

## Development Workflow

1. Make changes to the UI files
2. The development server will automatically reload
3. Test the changes in the browser
4. Once satisfied, build the site to verify production build:
   ```bash
   npm run build
   ```

## Style Guide

### Color Palette
- Background: `#0b0e14` (near-black)
- Surface: `#111827` (panels)
- Primary text: `#e5e7eb`
- Secondary text: `#9ca3af`
- Borders: `#1f2937`
- Accent: `#3b82f6` (blue)
- Accent hover: `#2563eb`

### Typography
- Font: system-ui or Inter
- Headings: 600-700 weight
- Body: 400 weight
- Max line length: ~70ch

### UI Rules
- No gradients
- No multiple accent colors
- Borders > shadows
- High contrast for readability
- No animations or emojis in chatbot