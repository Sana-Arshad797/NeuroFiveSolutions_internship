# AI-Powered Student Feedback Categorizer

A no-code automation that connects a Google Form to an AI model and
Google Sheets, so incoming student feedback is automatically categorized,
scored for sentiment, and summarized — without writing a custom
application.

**Status:** Workflow built and connected end-to-end in a live Zapier
account (Google Form → AI → Google Sheets). One real submission was
successfully processed through the full pipeline; two additional test
submissions are pending due to an OpenAI billing credit issue
encountered during testing. See `workflow/test-results.md` for the full,
honest breakdown of what succeeded, what failed, and why.

---

## 1. Project Overview

Students regularly submit free-text feedback about courses, labs, and
instructors. Reading through this feedback manually — figuring out what
it's about and how positive or negative it is — takes time and doesn't
scale well as submissions grow. This project automates that first pass:
every new form submission is automatically categorized, sentiment-scored,
and summarized by an AI model, with the result saved straight into a
spreadsheet.

## 2. Problem Being Solved

Manually reading and organizing open-ended student feedback is slow,
inconsistent (different reviewers might categorize the same feedback
differently), and easy to fall behind on. There's no built-in way in
Google Forms/Sheets alone to automatically understand *what* a piece of
feedback is about or *how* the student feels about it.

## 3. Objective

Build a real, working, no-code automation — using only a form, a
no-code automation platform, and an AI connector — that turns raw
feedback text into structured, actionable data (Category, Sentiment,
Summary) automatically, with no manual data entry.

## 4. Technologies / Tools Used

- **Google Forms** — collects the raw feedback (the trigger source).
- **Zapier** — the no-code automation platform that connects everything
  (free tier is sufficient for this workflow).
- **AI connector** — OpenAI, Claude, or Gemini via Zapier's built-in AI
  action step, used to analyze and structure the feedback.
- **Google Sheets** — stores the final, structured AI output.

## 5. Complete Workflow Architecture

```
Google Form
    |
    v
New Form Submission Trigger
    |
    v
Zapier
    |
    v
AI Analysis
    |
    v
Category + Sentiment + Summary
    |
    v
Google Sheets
```

## 6. Detailed Explanation of Every Workflow Step

1. **Google Form:** A student fills out a short feedback form (fields
   described in Section 7).
2. **Trigger:** Zapier watches the form (via its connected Google Sheet)
   for new responses and fires the Zap the moment a new one arrives.
3. **AI step:** Zapier sends the Course and Feedback text into an AI
   connector using the prompt documented in `workflow/ai-prompt.md`. The
   AI returns a Category, a Sentiment, and a short Summary.
4. **Final action:** Zapier writes a new row into a Google Sheet,
   combining the original submission data with the AI's structured
   output.

Full step-by-step build instructions are in `workflow/zapier-setup.md`.

## 7. Exact Fields Used in the Google Form

| Field | Type | Required? |
|---|---|---|
| Student Name | Short answer | Optional — kept optional so public demos and shared examples don't need to include real personal data |
| Course | Short answer / Dropdown | Required |
| Feedback | Paragraph (long answer) | Required |

## 8. AI Prompt Used

The full production prompt lives in `workflow/ai-prompt.md`, along with
an explanation of each part. In short, it instructs the AI to:

- Only use the Course and Feedback text as input (no Student Name).
- Classify feedback into one of six fixed categories.
- Determine sentiment as Positive, Neutral, or Negative.
- Write a short, factual, one-sentence summary.
- Return output in a strict, consistent format so it can be reliably
  mapped into spreadsheet columns.

## 9. Google Sheets Output Columns

| Column | Source |
|---|---|
| Timestamp | Form submission time (from the trigger) |
| Course | Form field |
| Feedback | Form field |
| AI Category | AI step output |
| AI Sentiment | AI step output |
| AI Summary | AI step output |

## 10. How the Workflow Was Tested

The workflow was tested by submitting real entries through the live
Google Form and checking: (1) whether the Zap ran successfully in
Zapier's Task History, and (2) whether a correctly filled-in row
appeared in the Google Sheet. Full details are in
`workflow/test-results.md`.

**Live execution status:**
- **1 submission succeeded end-to-end** — the Trigger, AI step, and
  Google Sheets step all completed, and a row was created in the "AI
  Feedback Results" sheet.
- **2 additional submissions were attempted but failed at the AI step**
  due to the connected OpenAI account running out of billing credits.
  These will be re-run and documented once credits are added (or the AI
  step is switched to Zapier's free built-in AI action).
- A formatting issue was also observed in the successful run (the AI
  Category column returned the sentiment value instead of the category)
  — see `workflow/test-results.md` for details and the fix needed.

## 11. Three Sample Test Events and Expected/Actual Outputs

| # | Course | Feedback | Expected Category | Expected Sentiment | Expected Summary |
|---|---|---|---|---|---|
| 1 | Cybersecurity | "The lab was very interesting and helped me understand network security." | Course/Lab | Positive | The lab helped the student understand network security. |
| 2 | Programming | "The assignment instructions were confusing and I wasn't sure what was required." | Assignment | Negative | The assignment instructions were unclear. |
| 3 | Database Systems | "The lectures are good, but some examples need more explanation." | Instructor | Neutral | Some lecture examples could use additional explanation. |

These are fictional sample cases used to demonstrate expected behavior.
Actual outputs from live runs go in `workflow/test-results.md`.

## 12. What the AI Step Contributes

Without the AI step, this would just be a form that dumps raw text into
a spreadsheet. The AI step is what turns unstructured feedback into
structured, usable data — consistently categorizing and scoring
sentiment the same way every time, and distilling long or rambling
feedback into a one-sentence summary that's quick to scan.

## 13. What Was Automated

- Detecting new feedback the moment it's submitted (no manual checking).
- Reading and interpreting free-text feedback.
- Assigning a consistent category and sentiment label.
- Writing a summary.
- Logging everything into a spreadsheet, ready for review or further
  analysis — with zero manual data entry.

## 14. Benefits of the Automation

- **Saves time** — no manual reading/tagging of every submission.
- **Consistency** — the AI applies the same categorization logic to
  every entry, unlike different human reviewers who might disagree.
- **Immediate visibility** — feedback appears in the spreadsheet, fully
  categorized, within moments of submission.
- **Scalable** — works the same whether 5 or 500 students submit
  feedback.
- **No coding required** — the entire pipeline is built and maintained
  through Zapier's visual interface.

## 15. Limitations

- The AI's categorization/sentiment judgment isn't perfect — ambiguous
  or mixed feedback may be classified in ways a human would disagree
  with.
- Relies on Zapier's free-tier task limits, which cap how many
  submissions can be processed per month.
- The AI only sees the text it's given — it has no broader context about
  the course, instructor, or student history.
- Structured output depends on the AI reliably following the requested
  format; occasional malformed responses may need a Zapier Formatter
  step or a retry to clean up.

## 16. Security / Privacy Considerations

- No API keys, OAuth tokens, or credentials are stored anywhere in this
  repository — all connections are configured directly and securely
  inside Zapier's own interface.
- Student Name is optional on the form and is **not** sent to the AI
  step at all — only Course and Feedback are used for analysis.
- All example data in this repository (`examples/`) is fictional and
  anonymized; no real student feedback or personal information is
  included.
- The AI prompt itself explicitly instructs the model to avoid exposing
  or repeating unnecessary personal information in its summaries.

## 17. Assignment Requirements Checklist

| Requirement | Status | Where documented |
|---|---|---|
| Real trigger selected (Google Form submission) | ✅ Documented | `workflow/workflow-overview.md` |
| No-code workflow built (Zapier, free-tier compatible) | ✅ Documented, ⏳ build pending | `workflow/zapier-setup.md` |
| AI step added (OpenAI/Claude/Gemini) | ✅ Documented | `workflow/ai-prompt.md` |
| Final action added (Google Sheets row) | ✅ Documented | `workflow/zapier-setup.md`, Section 9 above |
| Workflow tested with 2–3 real trigger events | ⚠️ Partial — 1 of 3 succeeded, 2 pending (OpenAI credits issue) | `workflow/test-results.md` |
| Screenshots captured | ⏳ To be completed live | `screenshots/README.md` |
| GitHub documentation completed | ✅ Complete | This repository |

**Legend:**
- ✅ = Prepared/documented in this repository.
- ⏳ = Requires actually running the live Zap in your own accounts —
  not something that can be pre-filled here.

## 18. Screenshots / Evidence Section

See `screenshots/README.md` for the full checklist of what to capture
and why. No screenshots are included yet; this section will be updated
with real evidence (Google Form, Zapier configuration, task history, and
Google Sheets results) once the workflow has been built and tested live.

## 19. What's Documentation vs. What's Live Evidence

To be fully transparent about the state of this project:

**Already prepared in this repository (documentation/design):**
- Full workflow architecture and explanation
- Google Form field design
- Google Sheets column design
- Complete, production-ready AI prompt
- Step-by-step Zapier build instructions
- Fictional sample test cases and expected outputs

**Already completed live:**
- The real Zap was built in a live Zapier account (Trigger → AI →
  Google Sheets).
- 1 of 3 planned test submissions was processed successfully end-to-end.

**Still needs to be collected/completed:**
- Adding OpenAI billing credits (or switching to Zapier's free built-in
  AI action) so the AI step stops failing.
- Fixing the Formatter step so AI Category and AI Sentiment don't return
  the same value.
- Re-running the 2 remaining pending test submissions.
- Capturing and adding real screenshots per `screenshots/README.md`.

## 20. Conclusion

This project demonstrates how a real, useful workflow — collecting and
understanding student feedback — can be automated end-to-end using only
no-code tools and a single AI processing step. The result is a system
that turns raw, unstructured feedback into clean, categorized data
automatically, without requiring any custom software development.

---

## Repository Structure

```
ai-student-feedback-automation/
│
├── README.md
├── workflow/
│   ├── workflow-overview.md
│   ├── zapier-setup.md
│   ├── ai-prompt.md
│   └── test-results.md
├── examples/
│   ├── sample-feedback.md
│   └── sample-output.md
├── screenshots/
│   └── README.md
└── .gitignore
```
