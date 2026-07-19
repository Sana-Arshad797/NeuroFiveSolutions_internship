# Few-Shot Prompt

## Task
Classify the same 10 customer support messages as **Complaint**, **Question**, or **Praise** — this time giving the model 3 labeled examples first.

## Prompt Used

```
Classify each customer support message as "Complaint", "Question", or "Praise".

Examples:
Message: "My order arrived broken and nobody has responded to my emails in 5 days."
Category: Complaint

Message: "How do I reset my password on the mobile app?"
Category: Question

Message: "Your support agent Sarah was incredibly helpful and solved my issue instantly, thank you!"
Category: Praise

Now classify the following 10 messages. Give only the category for each, numbered 1-10.

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
- This prompt was run as-is in **ChatGPT**, **Claude**, and **Gemini** — same 10 messages as the zero-shot test.
- The 3 examples were chosen to be unambiguous (one clear Complaint, one clear Question, one clear Praise) so the model learns the *pattern*, not just keywords.
- Outputs from each tool were recorded in `results-table.md`.
