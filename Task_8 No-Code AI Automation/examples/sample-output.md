# Sample Output (Expected AI Results — Fictional)

These show the AI output the workflow is *designed* to produce for each
sample in `sample-feedback.md`, based on the prompt in
`../workflow/ai-prompt.md`. These are illustrative/expected outputs, not
captured evidence from a live run — see `../workflow/test-results.md`
for the live-testing template.

---

### Sample 1

**Input (Course: Cybersecurity):**
"The lab was very interesting and helped me understand network
security."

**Expected AI Output:**
```
Category: Course/Lab
Sentiment: Positive
Summary: The lab helped the student understand network security.
```

---

### Sample 2

**Input (Course: Programming):**
"The assignment instructions were confusing and I wasn't sure what was
required."

**Expected AI Output:**
```
Category: Assignment
Sentiment: Negative
Summary: The assignment instructions were unclear.
```

---

### Sample 3

**Input (Course: Database Systems):**
"The lectures are good, but some examples need more explanation."

**Expected AI Output:**
```
Category: Instructor
Sentiment: Neutral
Summary: Some lecture examples could use additional explanation.
```

---

### Sample 4

**Input (Course: Web Development):**
"I couldn't submit my project because the upload portal kept giving an
error."

**Expected AI Output:**
```
Category: Technical Issue
Sentiment: Negative
Summary: The student was unable to submit their project due to an
upload portal error.
```

---

### Resulting Google Sheets Row (Example — Sample 1)

| Timestamp | Course | Feedback | AI Category | AI Sentiment | AI Summary |
|---|---|---|---|---|---|
| 2026-08-22 10:15 | Cybersecurity | The lab was very interesting and helped me understand network security. | Course/Lab | Positive | The lab helped the student understand network security. |
