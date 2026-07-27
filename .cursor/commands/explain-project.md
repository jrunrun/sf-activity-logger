# Explain Project

Provide a concise, high-level overview of the project so someone can understand and start using it quickly.

## Instructions

Analyze the codebase and return the following:

### 1. What This Project Does
- One-paragraph summary of the purpose
- Key use cases or problems it solves
- Who it's for (developers, end users, internal tools, etc.)

### 2. Tech Stack
- Frontend (frameworks, libraries)
- Backend (language, framework)
- Infrastructure (hosting, DB, APIs, services)
- Any notable tools (auth, AI/LLMs, messaging, etc.)

### 3. How to Run It
- Prerequisites (Node, Python, Docker, etc.)
- Environment variables required (mention `.env` if applicable)
- Install steps
- Run commands (dev + prod if available)

### 4. Project Structure (Quick Orientation)
- Key folders and what they contain
- Entry points (e.g., `main.py`, `app.tsx`, `server.js`)
- Where core logic lives

### 5. How to Quickly Explore
- What to open first (files, routes, UI entry points)
- Example flows (e.g., “login → dashboard → API call”)
- Any demo data or test endpoints

### 6. Notable Patterns / Architecture
- Auth approach (JWT, OAuth, etc.)
- Data flow (client → API → DB, etc.)
- Any unique or important design decisions

## Output Style
- Be concise and structured
- Use bullet points where possible
- Assume the reader is technical but new to the project
- Avoid unnecessary detail—optimize for quick understanding

## Optional Add-ons (if applicable)
- Common issues or gotchas
- Tips for local development
- Commands for debugging or logs

This command will be available in chat with /explain-project