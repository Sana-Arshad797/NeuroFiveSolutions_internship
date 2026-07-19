# Zero-Shot Prompt

## Task
Classify 10 customer support messages as **Complaint**, **Question**, or **Praise** — using only an instruction, no examples.

## Prompt Used

```
Classify each of the following customer support messages as "Complaint", "Question", or "Praise". Give only the category for each message, numbered 1-10.

1. "I've been waiting 3 days and still no response, is this normal?"
2. "Wow, didn't expect it to break so fast. Impressive."
3. "Can you tell me why my refund hasn't shown up yet?"
4. "Just wanted to say your support team fixed my issue in 5 minutes, amazing job!"
5. "Does this plan include free shipping or do I need to upgrade?"
6. "Not sure if this is a bug or I'm doing something wrong — the app crashes on login."
7. "Honestly the new update is so much better, finally!"
8. "This is the third time I'm messaging about the same problem."
9. "Quick one — how do I cancel my subscription?"
10. "Support was okay I guess, took a while but got sorted."
```

## Notes
- This prompt was run as-is in **ChatGPT**, **Claude**, and **Gemini**.
- No labeled examples were given — the model had to rely purely on its own understanding of the categories.
- Outputs from each tool were recorded in `results-table.md`.
