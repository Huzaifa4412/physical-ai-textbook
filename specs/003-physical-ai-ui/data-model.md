# Data Model: Physical AI & Humanoid UI

## Overview
This document defines the data structures and entities for the Physical AI & Humanoid UI feature, focusing on the UI state and content structures.

## UI State Entities

### Homepage State
- **heroSection**: Object containing hero section content
  - title: string (required) - "Physical AI & Humanoid Systems"
  - subtitle: string (required) - Technical subtitle content
  - supportingText: string (optional) - Supporting line content
  - primaryCta: object
    - text: string (required) - "Start Reading"
    - style: string (required) - "solid accent color"
  - secondaryCta: object
    - text: string (required) - "View Book Structure"
    - style: string (required) - "outline / subtle"

### Scope Section State
- **scopeCards**: Array of card objects
  - title: string (required) - Card title
  - description: string (required) - Card description
  - type: enum (required) - ["Production Focused", "Agentic Systems", "End-to-End"]

### Learning Path State
- **learningPath**: Array of path objects
  - step: number (required) - Sequential order
  - title: string (required) - Path element title
  - description: string (optional) - Detailed description

## UI Configuration Entities

### Theme Configuration
- **theme**: Object containing styling properties
  - background: string (required) - "#0b0e14" (near-black)
  - surface: string (required) - "#111827" (panels)
  - primaryText: string (required) - "#e5e7eb"
  - secondaryText: string (required) - "#9ca3af"
  - borders: string (required) - "#1f2937"
  - accent: string (required) - "#3b82f6" (blue)
  - accentHover: string (required) - "#2563eb"

### Chat Assistant Configuration
- **chatConfig**: Object containing assistant properties
  - title: string (required) - "Physical AI Assistant"
  - position: string (required) - "bottom-right"
  - autoOpen: boolean (required) - false
  - tone: string (required) - "calm, technical"
  - emojiAllowed: boolean (required) - false
  - animationsAllowed: boolean (required) - false

## Content Entities

### Book Structure Content
- **bookSections**: Array of section objects
  - title: string (required) - Section title
  - description: string (required) - Section description
  - topics: array of strings (required) - Covered topics
  - priority: enum (required) - ["P1", "P2", "P3"]

### Typography Configuration
- **typography**: Object containing font properties
  - fontFamily: string (required) - "system-ui or Inter"
  - headingWeight: range (required) - 600-700
  - bodyWeight: number (required) - 400
  - maxLineLength: string (required) - "~70ch"