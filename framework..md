# AI Content Storytelling Graph Framework

This document defines structured storytelling graphs for automated AI content generation.

Each content category follows a node-based storytelling flow.

---

## MASTER STORY PRINCIPLE

All content follows this core structure:

HOOK → CONTEXT → VALUE → EXAMPLE → TAKEAWAY → CTA

---

# 1. New Tools Introduction

## Story Graph

[SCROLL HOOK]
    ↓
[User Problem / Pain Point]
    ↓
[Tool Introduction]
    ↓
[Unique Differentiator]
    ↓
[Real Use Case / Demo]
    ↓
[Why It Matters Now]
    ↓
[Call To Action]

## Purpose

- Introduce new AI tools
- Generate curiosity
- Fast awareness content

---

# 2. Tool Detailed Explanation (How To Use)

## Story Graph

[Hook]
    ↓
[Problem Statement]
    ↓
[Tool Overview]
    ↓
[Step 1]
    ↓
[Step 2]
    ↓
[Step 3]
    ↓
[Pro Tips]
    ↓
[Common Mistakes]
    ↓
[Final Result]
    ↓
[CTA]

## Purpose

- Educational content
- Tutorials
- Walkthrough videos

---

# 3. Trending AI Models

## Story Graph

[Breaking Hook]
    ↓
[Model Introduction]
    ↓
[Key Innovation]
    ↓
[Performance Insight]
    ↓
[Real World Applications]
    ↓
[Target Users]
    ↓
[Future Impact]
    ↓
[CTA]

## Purpose

- Highlight AI breakthroughs
- Technical insights simplified

---

# 4. AI Trending News (X / Twitter Trends)

## Story Graph

[Viral Hook]
    ↓
[What Happened]
    ↓
[Why It Is Trending]
    ↓
[Simplified Explanation]
    ↓
[Industry Impact]
    ↓
[Expert Insight / Opinion]
    ↓
[CTA]

## Purpose

- Fast news content
- Trend analysis

---

# 5. GitHub Open Source Repository

## Story Graph

[Hook]
    ↓
[Repository Overview]
    ↓
[Core Features]
    ↓
[Why Developers Like It]
    ↓
[Use Case Example]
    ↓
[Trend Signals (Stars / Adoption)]
    ↓
[CTA]

## Purpose

- Developer-focused content
- Open source discovery

---

# 6. Instagram Engagement Content

## Story Graph

[Relatable Hook]
    ↓
[Quick Insight]
    ↓
[Simple Example]
    ↓
[Audience Question]
    ↓
[Micro Takeaway]
    ↓
[CTA]

## Purpose

- Increase engagement
- Boost saves and shares

---

# Implementation Tip (For RAG Application)

Store story flows as structured nodes:

{
  "category": "new_tool_intro",
  "story_flow": [
    "hook",
    "problem",
    "tool_intro",
    "unique_value",
    "use_case",
    "why_now",
    "cta"
  ]
}

AI should generate content by filling each node sequentially.

---

END OF DOCUMENT
