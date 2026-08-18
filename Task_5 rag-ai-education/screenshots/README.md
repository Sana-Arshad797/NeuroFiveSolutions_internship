# Screenshots Guide

This folder should contain screenshots that provide visual proof of the RAG workflow described in the main `README.md` and `PROJECT_REPORT.md`. These screenshots must be captured personally — none have been generated as part of this project, since only real, actual screenshots of your own Claude conversation and GitHub repository should be used as evidence.

## Required Screenshots

```text
screenshots/
├── 01-document-upload.png
├── 02-question-answer.png
├── 03-hallucination-test.png
└── 04-github-repository.png
```

### 01-document-upload.png
A screenshot showing the source PDF (`source-document.pdf`) being uploaded to Claude, or the confirmation that Claude has received and can see the document. This proves the private document was actually used as the knowledge source.

### 02-question-answer.png
A screenshot showing at least one of the questions from the "Questions and Answers" section being asked in Claude, along with the model's grounded answer (ideally including a page/section reference in the response). Capture one clear, readable example — you do not need to screenshot all seven questions.

### 03-hallucination-test.png
A screenshot showing the unsupported-question test being run (e.g., asking about the South Korea teacher-adoption statistic from Section "Unsupported Information Test") and Claude correctly responding that the information is not available in the document. This is the most important screenshot for proving the system does not hallucinate.

### 04-github-repository.png
A screenshot of the completed GitHub repository page, showing the file structure (`README.md`, `PROJECT_REPORT.md`, `source-document.pdf`, and the `screenshots/` folder) after everything has been uploaded and committed.

## Notes

- Screenshots should be clear, readable, and in PNG or JPG format.
- Crop out any unrelated personal information (e.g., browser tabs, email addresses, notifications) before saving.
- If your assignment requires additional screenshots (for example, one per question), you may add them here using a similar naming pattern (e.g., `05-question-2.png`, `06-question-3.png`).
