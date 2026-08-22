# Workflow Overview

This document summarizes the end-to-end automation in a single, quick-read
format. For full setup instructions see `zapier-setup.md`, and for the AI
prompt itself see `ai-prompt.md`.

## Trigger

**Event:** New Google Form response.
**Platform:** Google Forms → connected to Zapier via the Google Forms
trigger app.
**Trigger type:** "New Response in Spreadsheet" / "New Form Response"
(Google Forms trigger in Zapier).

## Input Data

Each form submission provides:

| Field | Description |
|---|---|
| Student Name | Optional. Not required for the automation to work. |
| Course | The course the feedback relates to. |
| Feedback | Free-text feedback from the student. |

Only **Course** and **Feedback** are sent to the AI step. Student Name is
collected for optional internal reference but is intentionally excluded
from the AI prompt and from public examples in this repository.

## AI Processing

**Platform:** OpenAI (or Claude/Gemini — any Zapier-supported AI
connector works the same way).
**Action:** Zapier's AI connector step (e.g. "OpenAI — Conversation" /
"ChatGPT" action).
**Input to AI:** Course + Feedback text, inserted into the prompt defined
in `ai-prompt.md`.
**Output from AI:** Three structured fields:

- **Category** — one of: Course/Lab, Instructor, Assignment, Resources,
  Technical Issue, Other
- **Sentiment** — Positive, Neutral, or Negative
- **Summary** — a short, factual, one-sentence summary

## Output → Final Action

**Platform:** Google Sheets.
**Action:** "Create Spreadsheet Row."
**What happens:** The AI's Category, Sentiment, and Summary — along with
the original Timestamp, Course, and Feedback — are written as a new row
in a Google Sheet.

## End-to-End Flow

```
Student fills out Google Form
        |
        v
Zapier detects new form response (Trigger)
        |
        v
Zapier sends Course + Feedback to the AI step
        |
        v
AI returns: Category, Sentiment, Summary
        |
        v
Zapier writes a new row to Google Sheets:
Timestamp | Course | Feedback | AI Category | AI Sentiment | AI Summary
```

This is a fully no-code pipeline: no custom application code is used to
run the workflow. Zapier handles the trigger, the AI call, and the final
spreadsheet write, based purely on configuration.
