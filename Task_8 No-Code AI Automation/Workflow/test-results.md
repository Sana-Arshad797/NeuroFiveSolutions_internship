# Test Results

> **Status: Partially tested — 1 live run completed, additional runs
> pending.** The workflow was built and connected end-to-end (Google
> Form → Zapier → AI → Google Sheets) and successfully processed one
> real submission. Two further submissions were sent but failed at the
> AI step because the OpenAI account ran out of API credits (see the
> "Issue Encountered" note below). Those rows are marked accordingly and
> will be re-run once credits are added.

## Live Test Run #1 — Successful ✅

| Field | Value |
|---|---|
| Timestamp | 2026-08-22 11:40:06 |
| Course | Cyber security |
| Feedback | "Course was just amazing and I've learned..." (student's full submitted text) |
| AI Category (returned) | Positive |
| AI Sentiment (returned) | Positive |
| AI Summary (returned) | The student found the course amazing and learned a lot from it. |
| Zapier result | Success — all 3 steps (Trigger → AI → Sheets) completed and a new row was created |
| Google Sheets result | Row confirmed in "AI Feedback Results" sheet |

**Observation / known issue:** The AI returned "Positive" in the **AI
Category** field, when it should have returned a category such as
"Course/Lab" — the Sentiment value appears to have been duplicated into
the Category field. This points to a formatting/pattern-matching issue
in the Zapier Formatter step used to split the AI's combined response
into separate Category/Sentiment/Summary values, rather than an issue
with the AI's classification itself. This is documented here as an
honest record of the workflow's current behavior and a limitation to
fix (see `workflow/zapier-setup.md`, Step 8, and Section 15 of the main
README).

## Live Test Runs #2 and #3 — Attempted, Failed at AI Step ⚠️

Two additional live submissions were sent through the real Google Form,
but the Zapier AI (OpenAI) step returned an error:

```
This ChatGPT (OpenAI) step hit an error
You have no credits remaining. Add credits to continue using the API.
```

As a result, these submissions did not reach the Google Sheets step and
no rows were created for them. This is documented honestly rather than
fabricated — these two test cases will be re-run and this section
updated once OpenAI billing credits are added (or once the workflow is
switched to Zapier's built-in free AI action).

## Planned Test Cases (for re-run once the credit issue is resolved)

| Test # | Input Feedback | Expected Category | Expected Sentiment | Expected Summary | Zapier Result | Google Sheets Result |
|---|---|---|---|---|---|---|
| 2 | "The assignment instructions were confusing and I wasn't sure what was required." (Course: Programming) | Assignment | Negative | The assignment instructions were unclear. | Failed — OpenAI out of credits | Not created (step failed before reaching Sheets) |
| 3 | "The lectures are good, but some examples need more explanation." (Course: Database Systems) | Instructor | Neutral | Some lecture examples could use additional explanation. | Failed — OpenAI out of credits | Not created (step failed before reaching Sheets) |

## Next Steps to Complete Testing

1. Add OpenAI billing credits (https://platform.openai.com/settings/organization/billing/)
   **or** switch the AI step to Zapier's built-in "AI by Zapier" action,
   which doesn't require a paid API key.
2. Fix the Formatter step so "AI Category" correctly extracts the
   category value instead of duplicating the sentiment value.
3. Re-submit the two pending test cases through the live form.
4. Update this file with the real results from those runs.

## How to Fill This In After Testing

1. Submit each test case through the real, live Google Form.
2. Open Zapier → your Zap → **Task History**.
3. For each run, record in the "Zapier result" column:
   - Whether the run succeeded or failed.
   - The exact Category / Sentiment / Summary the AI step returned.
4. Open the "AI Feedback Results" Google Sheet and, for the "Google
   Sheets result" column, record:
   - Whether a new row appeared correctly.
   - Whether all six columns were populated as expected.
5. Note any discrepancies between the *expected* and *actual* results
   (e.g. the AI chose a different category than predicted) — this kind
   of comparison is valuable evidence of how the automation performs in
   practice.

## Testing Notes Section

Use this space to record any observations while testing (e.g. edge
cases, formatting issues, AI response inconsistencies):

```
(To be filled after live testing)
```
