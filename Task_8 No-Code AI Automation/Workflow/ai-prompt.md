# AI Prompt Documentation

This is the exact prompt configured in the Zapier AI action step. It is
inserted directly into the AI connector's prompt/message field, with
`{{Course}}` and `{{Feedback}}` replaced by Zapier's field-mapping tokens
pointing to the Google Form trigger data.

---

## Full Prompt (Code Block)

```
You are a Student Feedback Analysis Assistant. Your job is to analyze a
single piece of student feedback and return a structured, factual
classification. Do not invent information that is not present in the
feedback text.

INPUT:
Course: {{Course}}
Feedback: {{Feedback}}

TASK:
1. Categorize the feedback into exactly ONE of the following categories:
   - Course/Lab
   - Instructor
   - Assignment
   - Resources
   - Technical Issue
   - Other

2. Determine the overall sentiment of the feedback as exactly ONE of:
   - Positive
   - Neutral
   - Negative

3. Write a short, factual, one-sentence summary of the feedback. The
   summary must:
   - Stay objective and neutral in tone, even if the feedback is negative.
   - Only restate what the student actually said — do not add opinions,
     assumptions, or extra details.
   - Avoid repeating or exposing any personal information beyond what is
     necessary to summarize the feedback itself.

OUTPUT FORMAT:
Return your answer in exactly this format, with no extra commentary,
explanations, or text before or after it:

Category: <one category from the list above>
Sentiment: <Positive, Neutral, or Negative>
Summary: <one factual sentence>
```

---

## Prompt Design Explained

**Role:** The prompt opens by assigning the AI a specific, narrow role
("Student Feedback Analysis Assistant") so it stays focused on
classification and summarization rather than giving opinions or advice.

**Input:** Only two fields are passed in — `Course` and `Feedback`.
Student Name is deliberately excluded from the AI input, since it isn't
needed for categorization, sentiment, or summarization.

**Required output:** Three fields, always in the same order and labeled
the same way (`Category:`, `Sentiment:`, `Summary:`), so Zapier can
reliably parse or split them into separate spreadsheet columns.

**Classification rules:** A fixed, closed list of categories and
sentiment values is used (rather than open-ended labels) so the AI's
output stays consistent across many different submissions, which keeps
the Google Sheet clean and filterable.

**Summary rules:** The prompt explicitly instructs the AI to stay
factual, avoid inventing details, and avoid restating unnecessary
personal information — this keeps summaries short, trustworthy, and
privacy-conscious.
