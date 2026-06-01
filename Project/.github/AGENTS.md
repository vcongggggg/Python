# AI Agents Guide

This document defines the agents used in this project and how to work with them.

## Scope
- Applies to AI-assisted development for the Django bookstore + Ollama chatbot.
- Use for onboarding and consistent collaboration.

## Agent Roster
1. **Planner**
   - Turns product requirements into an implementation plan.
   - Outputs a task list and identifies risks/dependencies.

2. **Research**
   - Checks docs/specs and existing code patterns before changes.
   - Summarizes findings with links to files and decisions.

3. **Implementation**
   - Makes code changes following project conventions.
   - Keeps edits minimal and testable.

4. **QA / Testing**
   - Defines test strategy (unit/integration/e2e where relevant).
   - Runs tests and reports results with clear reproduction steps.

5. **Security**
   - Reviews input validation, auth, secrets, and data handling.
   - Flags risks and proposes safer alternatives.

6. **UI/UX**
   - Ensures templates and styles match the design direction.
   - Checks responsive behavior and accessibility basics.

## Operating Rules
- Prefer small, reviewable changes over large refactors.
- Avoid destructive commands (e.g., hard reset) unless explicitly approved.
- Do not modify production data or credentials.
- Validate user input at system boundaries.
- Keep prompts and outputs in Vietnamese where the UI is Vietnamese.

## Runbook (Typical Flow)
1. **Planner** creates a plan and identifies files to touch.
2. **Research** checks docs and existing code paths.
3. **Implementation** applies changes and updates templates/views as needed.
4. **QA / Testing** runs tests or provides manual test steps.
5. **Security** reviews any changes involving user input, auth, or external calls.

## File Conventions
- Django code in `books/` and `bookstore/`.
- Templates under `templates/`.
- Static assets under `static/`.
- Ollama settings live in `bookstore/settings.py`.

## Output Expectations
- Provide concise change summaries.
- Include file references and line ranges when applicable.
- Offer test commands or verification steps.

## Escalation
- If requirements are unclear, ask for clarification before coding.
- If a change impacts data or security, request approval first.
