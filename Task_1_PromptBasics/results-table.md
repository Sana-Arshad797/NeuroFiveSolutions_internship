# Results Comparison — Zero-Shot vs Few-Shot

## Correct (Expected) Labels

| # | Message | Expected Category |
|---|---------|-------------------|
| 1 | I've been waiting 3 days and still no response, is this normal? | Complaint |
| 2 | Wow, didn't expect it to break so fast. Impressive. | Complaint |
| 3 | Can you tell me why my refund hasn't shown up yet? | Question |
| 4 | Just wanted to say your support team fixed my issue in 5 minutes, amazing job! | Praise |
| 5 | Does this plan include free shipping or do I need to upgrade? | Question |
| 6 | Not sure if this is a bug or I'm doing something wrong — the app crashes on login. | Complaint |
| 7 | Honestly the new update is so much better, finally! | Praise |
| 8 | This is the third time I'm messaging about the same problem. | Complaint |
| 9 | Quick one — how do I cancel my subscription? | Question |
| 10 | Support was okay I guess, took a while but got sorted. | Complaint |

---

## Zero-Shot Results

| # | ChatGPT | Claude | Gemini |
|---|---------|--------|--------|
| 1 | Complaint | Complaint |Complaint  |
| 2 | Complaint |Complaint  |Complaint  |
| 3 | Question | Question | Question |
| 4 | Praise |Praise  | Praise |
| 5 | Question |Question  |Question  |
| 6 | Complaint | Question | Complaint |
| 7 |  Praise| Praise | Praise |
| 8 | Complaint |Complaint  | Complaint |
| 9 | Question | Question | Question |
| 10 | Praise | Complaint |Praise  |
| **Accuracy** | 9/10 | 9/10 | 9/10 |

*(Screenshot: `zero-shot-chatgpt.jpg`, `zero-shot-claude.jpg`, `zero-shot-gemini.jpg`)*

---

## Few-Shot Results

| # | ChatGPT | Claude | Gemini |
|---|---------|--------|--------|
| 1 |Complaint  |Complaint  | Complaint |
| 2 |Complaint  | Complaint | Complaint |
| 3 | Question |  Question | Question |
| 4 | Praise |  Praise | Praise |
| 5 |Question  |  Question | Question |
| 6 |Complaint  | Question  | Complaint |
| 7 | Praise |  Praise |Praise  |
| 8 |Complaint  | Complaint |Complaint  |
| 9 | Question | Question  | Question |
| 10 | Complaint | Complaint |Praise  |
| **Accuracy** | 10/10 | 9/10 | 9/10 |

*(Screenshot: `few-shot-chatgpt.jpg`, `few-shot-claude.jpg`, `few-shot-gemini.jpg`)*

---

## Overall Accuracy Summary

| Tool | Zero-Shot Accuracy | Few-Shot Accuracy | Improvement |
|------|--------------------|--------------------|-------------|
| ChatGPT | 9/10 | 10/10 | +1 |
| Claude | 9/10 | 9/10 | +0(no change) |
| Gemini | 9/10 | 9/10 | +0(no change) |

---

## Takeaway (3-4 sentences)

Few-shot prompting improved accuracy across chatgpt, particularly on messages with sarcasm or mixed sentiment (like #10), because the labeled examples gave the model a clearer pattern to follow instead of relying on surface-level keywords. Zero-shot prompts struggled most with messages that combined a question and a complaint together (#3, #6), often misclassifying them. chatgpt showed the biggest jump in accuracy, while all three tools performed well even in zero-shot. This confirms that showing examples matters more than writing a longer or more detailed instruction.
