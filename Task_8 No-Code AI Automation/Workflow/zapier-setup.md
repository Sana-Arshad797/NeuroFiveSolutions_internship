# Zapier Setup Guide (Step-by-Step)

This guide walks through building the actual Zap manually. It assumes no
prior Zapier experience.

---

## Step 1 — Create the Google Form

1. Go to [forms.google.com](https://forms.google.com) and create a new
   form titled **"Student Feedback Form."**
2. Add these fields:
   - **Student Name** — Short answer, marked *optional*.
   - **Course** — Short answer or Dropdown (recommended: Dropdown with
     your course list, to keep data consistent).
   - **Feedback** — Paragraph (long answer).
3. Under the form's **Responses** tab, click the Google Sheets icon to
   link responses to a new spreadsheet (this creates a raw-responses
   sheet — separate from the AI-results sheet in Step 2).

## Step 2 — Create the Google Sheet (AI results)

1. Create a new, separate Google Sheet named **"AI Feedback Results."**
2. In row 1, add these column headers exactly:
   ```
   Timestamp | Course | Feedback | AI Category | AI Sentiment | AI Summary
   ```
3. Leave the rest of the sheet empty — Zapier will populate rows
   automatically.

## Step 3 — Connect Google Forms to Zapier

1. Log into [zapier.com](https://zapier.com) (free tier is sufficient).
2. Click **Create Zap**.
3. Search for and select **Google Forms** as the Trigger app.
4. Choose the trigger event **"New Response in Spreadsheet"** (or "New
   Form Response," depending on the current Zapier UI).
5. Connect your Google account when prompted and authorize access.

## Step 4 — Create the Trigger

1. Select the specific form created in Step 1 as the trigger source.
2. Zapier will ask you to pull in a sample response — submit one test
   response on your form first if none exist yet.

## Step 5 — Test the Trigger

1. Click **Test trigger** in Zapier.
2. Confirm Zapier successfully retrieves your sample Course and Feedback
   fields.

## Step 6 — Add the AI Action

1. Click **+** to add a new step.
2. Search for your chosen AI connector (**OpenAI**, **Claude**, or
   **Gemini** — all work the same way conceptually).
3. Choose an action such as **"Conversation"** (OpenAI) or the
   equivalent "send a prompt" action for your chosen provider.
4. Connect your AI account (API key is entered directly into Zapier's
   secure connection screen — it is never stored in this repository).

## Step 7 — Insert Form Fields into the AI Prompt

1. Open the prompt field in the AI action.
2. Paste in the full prompt from `ai-prompt.md`.
3. Where the prompt says `{{Course}}` and `{{Feedback}}`, use Zapier's
   field-insertion menu to map in the actual **Course** and **Feedback**
   fields from Step 4's trigger data.

## Step 8 — Configure Structured AI Output

1. In the AI action's settings, keep the response format instructions
   from the prompt (Category / Sentiment / Summary, one per line).
2. Set a reasonable max token limit (e.g. 150–200) since output must
   stay short.
3. Run a test of this step and confirm the AI returns all three fields
   in the expected format.

## Step 9 — Add the Google Sheets Action

1. Click **+** to add another step.
2. Search for **Google Sheets** as the action app.
3. Choose the action event **"Create Spreadsheet Row."**
4. Connect your Google account and select the **"AI Feedback Results"**
   spreadsheet and worksheet from Step 2.

## Step 10 — Map AI Outputs to Spreadsheet Columns

Map each spreadsheet column to the corresponding data:

| Sheet Column | Mapped From |
|---|---|
| Timestamp | Trigger step → form submission timestamp |
| Course | Trigger step → Course field |
| Feedback | Trigger step → Feedback field |
| AI Category | AI step → Category (parsed from AI output) |
| AI Sentiment | AI step → Sentiment (parsed from AI output) |
| AI Summary | AI step → Summary (parsed from AI output) |

> If the AI returns Category/Sentiment/Summary as one text block, use
> Zapier's built-in **Formatter** step (Text → Extract Pattern, or
> Split Text) between the AI step and the Sheets step to separate them
> into three distinct values before mapping.

## Step 11 — Test the Action

1. Click **Test action** on the Google Sheets step.
2. Confirm a new row appears correctly in your Google Sheet with all six
   columns filled in.

## Step 12 — Turn On the Zap

1. Name the Zap (e.g. "Student Feedback → AI → Sheets").
2. Toggle the Zap **ON**.

## Step 13 — Submit 2–3 Real Test Forms

1. Open your live Google Form (not the Zapier test data) and submit at
   least 2–3 realistic but fictional feedback entries.
2. Use different courses and different sentiment types (positive,
   neutral, negative) to demonstrate the AI's classification range.

## Step 14 — Verify the Rows in Google Sheets

1. Open the "AI Feedback Results" sheet.
2. Confirm each test submission produced a new row with a sensible
   Category, Sentiment, and Summary.

## Step 15 — Capture Screenshots

Follow the checklist in `screenshots/README.md` to document each stage
of the working Zap for your submission.
