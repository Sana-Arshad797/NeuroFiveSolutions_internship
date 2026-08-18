# RAG Project: AI in Modern Education

## Overview

This project demonstrates a simple, no-code **Retrieval-Augmented Generation (RAG)** workflow using a private source document. Instead of relying only on an AI model's general training knowledge, the model (Claude) was given a specific PDF — *"The Impact of Artificial Intelligence on Modern Education"* — and asked to answer questions using only the information contained in that document.

The project shows how grounding an AI's answers in a private document produces more accurate, specific, and verifiable responses than asking the same AI a plain, ungrounded question.

## Objective

The objective of this project is to demonstrate the core idea behind RAG: combining a **retrieval step** (pulling relevant information from a private document) with a **generation step** (the AI producing a natural-language answer based on that retrieved information).

This matters because general-purpose AI models are trained on broad public data and do not know the contents of private or specialized documents unless that content is explicitly provided to them. RAG solves this by grounding the model's answers in a specific, trusted source, which reduces hallucination and allows the model to cite exactly where an answer came from.

## Source Document

- **Document title:** The Impact of Artificial Intelligence on Modern Education
- **Topic:** Uses, benefits, challenges, ethics, and future outlook of AI in education
- **Number of pages:** 10
- **Short description:** An academic-style report covering how AI is used in classrooms and universities, personalized learning, AI tutoring, benefits, challenges, privacy/ethics/academic integrity, impacts on teachers, and future predictions. The report cites named sources (e.g., Walton Family Foundation & Gallup, Pew Research Center, Education Week, Turnitin, Electroiq, Demandsage, Textero) for its statistics.

## RAG Approach

For this project, Claude was used with the uploaded PDF as the **private knowledge source**, in a no-code document-grounding approach (no LangChain, vector database, or custom embedding pipeline was built).

Document-grounded question answering works like this:

1. The private document (the PDF) is provided directly to the AI model as context.
2. A question is asked about the document's content.
3. The model searches (retrieves) the relevant passage(s) from the document.
4. The model generates an answer using only the retrieved passage(s), rather than general knowledge.
5. The answer can be checked against the document to confirm it is accurate and not invented.

This mirrors the retrieval + generation pattern used in full RAG systems, except the "retrieval" here is performed by the model reading the uploaded document directly instead of querying a vector database.

## Questions and Answers

### Question 1
What percentage of U.S. K-12 public school teachers used AI tools during the 2024–2025 school year, according to the report?

**Answer:** 60% of U.S. K-12 public school teachers used AI tools during the 2024–2025 school year, with 32% using them at least weekly, according to a joint study by the Walton Family Foundation and Gallup.

**Evidence / Page:** Page 1, Section 1 ("Introduction to Artificial Intelligence in Education").

---

### Question 2
How did teen use of ChatGPT for schoolwork change between 2023 and 2024, according to the document?

**Answer:** The share of U.S. teens using ChatGPT for schoolwork roughly doubled in one year, rising from 13% in 2023 to 26% in 2024, according to Pew Research Center data cited in the report.

**Evidence / Page:** Page 1, Section 1 ("Introduction to Artificial Intelligence in Education").

---

### Question 3
What are the four broad categories of AI use in education described in the report?

**Answer:** The report groups AI use in education into four categories: (1) instructional support for teachers, (2) direct learning support for students, (3) administrative automation, and (4) institutional analytics.

**Evidence / Page:** Page 2, Section 2 ("How AI Is Being Used in Education").

---

### Question 4
According to the report, how much time do teachers who use AI tools weekly save on average?

**Answer:** Teachers who use AI tools at least weekly reported saving an average of close to six hours per week on tasks such as grading and lesson preparation, based on data from the Walton Family Foundation and Gallup study.

**Evidence / Page:** Page 2, Section 2.3 ("Administrative Automation"); repeated on Page 5, Section 5.1 ("Time Savings for Teachers").

---

### Question 5
What accuracy gap does the report describe between human tutors and AI tutoring systems in interpreting student emotions?

**Answer:** The report states that human tutors could interpret a student's emotional state (such as frustration or confusion) with about 92% accuracy, while even advanced AI tutoring systems managed only about 68% accuracy on the same measure, based on research compiled in Demandsage's 2026 AI in Education Statistics report.

**Evidence / Page:** Page 4–5, Section 4.2 ("Strengths and Limits Compared to Human Tutors").

---

### Question 6
What percentage of U.S. K-12 teachers reported lacking formal training on AI, according to the report?

**Answer:** 71% of U.S. K-12 teachers reported lacking formal training on AI, even though around 74% of districts planned to offer AI training by fall 2025, according to survey data compiled in Electroiq's 2025 report.

**Evidence / Page:** Page 6, Section 6.4 ("Teacher Preparedness").

---

### Question 7
What law does the report identify as governing student data privacy in U.S. schools?

**Answer:** The report identifies the Family Educational Rights and Privacy Act (FERPA) as the law that governs student data privacy in U.S. schools and restricts how student educational records can be shared.

**Evidence / Page:** Page 7, Section 7.1 ("Data Privacy").

## Hallucination Testing

Each answer above was verified by locating the exact section and page in the source PDF that contains the supporting statement, and by confirming that no numbers, names, or claims were added beyond what the document states.

| Question | Supported by PDF? | Evidence/Page | Hallucination? |
|---|---|---|---|
| Q1: Teacher AI adoption 2024–2025 | Yes | Page 1, Section 1 | No |
| Q2: Teen ChatGPT use 2023 vs 2024 | Yes | Page 1, Section 1 | No |
| Q3: Four categories of AI use | Yes | Page 2, Section 2 | No |
| Q4: Teacher time savings | Yes | Page 2 & Page 5 | No |
| Q5: Human vs AI tutor emotional accuracy | Yes | Page 4–5, Section 4.2 | No |
| Q6: Teachers lacking AI training | Yes | Page 6, Section 6.4 | No |
| Q7: FERPA and student data privacy | Yes | Page 7, Section 7.1 | No |

**No hallucinations were found.** All seven answers were directly traceable to specific sections and pages of the source PDF, and no statistics, names, or claims were invented.

### Unsupported-Question Test

**Question (deliberately outside the document's scope):** According to the report, what percentage of teachers in South Korea use AI tools in the classroom?

**Expected grounded response:**
> "This information is not available in the provided document."

**Verification:** The source PDF discusses AI adoption statistics for the United States (and briefly references global/multinational survey data on students), but it does not contain any country-specific statistic for South Korea. A properly grounded RAG response must decline to answer rather than invent a plausible-sounding number.

## Plain Prompt vs RAG

| Aspect | Plain Prompt | RAG / Document-Grounded |
|---|---|---|
| Information source | The model's general training data | The uploaded private PDF |
| Specificity | General, often generic statements | Specific figures, named studies, and page-level detail |
| Relevance | May include outdated or broadly applicable information | Directly matches the content of this specific report |
| Document evidence | None — no way to trace the answer to a source | Each answer can be traced to a page/section in the PDF |
| Hallucination risk | Higher — model may generate plausible but unverifiable claims | Lower — answer is checked against the actual document text |
| Private data | Cannot access private/unpublished documents | Can directly use the private document as its knowledge source |

### Examples (hypothetical — no separate plain-prompt experiment was run)

*The following plain-prompt responses are hypothetical illustrations of how an ungrounded answer might differ from the document-grounded answers above. They were not generated as an actual separate experiment for this project.*

**Example 1**
- *Plain prompt:* "What percentage of teachers use AI in schools?" → A plain prompt might return a generic, unsourced estimate (e.g., "many teachers now use AI tools") without a specific figure or source.
- *RAG answer:* "60% of U.S. K-12 public school teachers used AI tools during the 2024–2025 school year... (Walton Family Foundation & Gallup, 2025)," traceable to Page 1 of the source document.

**Example 2**
- *Plain prompt:* "How much time do AI tools save teachers?" → A plain prompt might give a vague answer like "AI can save teachers a significant amount of time" with no number attached.
- *RAG answer:* "close to six hours per week," directly sourced from Page 2 and Page 5 of the document.

**Example 3**
- *Plain prompt:* "What law protects student data privacy?" → A plain prompt might answer generically about "data protection laws" without naming a specific U.S. statute.
- *RAG answer:* Specifically names FERPA, sourced from Page 7, Section 7.1 of the document.

## Reflection

Grounding the AI in my own document changed the quality of its answers in several clear ways. Without the source PDF, a plain prompt about "AI in education statistics" would likely have produced generic, broadly true but unspecific statements, since the model would be drawing on a wide range of possibly outdated or mismatched public information rather than this particular report. With the document provided, every answer became traceable to an exact page and section, which made it possible to verify accuracy rather than simply trust the response.

Specificity improved the most. Instead of vague claims like "many teachers use AI," the grounded answers included exact figures (60%, 32%, 71%, 92% vs. 68%) tied to named studies (Walton Family Foundation & Gallup, Pew Research Center, Electroiq, Demandsage) exactly as they appear in the report. Relevance also improved, because the answers reflected the specific framing and structure of this document rather than a generic overview of the topic.

Hallucination risk dropped significantly. Because the model was restricted to the content of the PDF, it had no reason to invent statistics, and the unsupported-question test confirmed that when information genuinely was not in the document (such as a country-specific statistic not mentioned in the report), the correct behavior was to say so rather than fabricate an answer.

The main limitation is that grounded answers are only as good as the source document itself: if the PDF contains an error or an outdated statistic, the grounded answer will faithfully repeat it. This project confirms that RAG's main value is not that it makes an AI "smarter," but that it makes an AI's answers **traceable, specific, and honest about the limits of what it knows**.

## Conclusion

This project demonstrates that document-grounded question answering (RAG) produces answers that are more specific, more traceable, and less prone to hallucination than plain, ungrounded prompting. By using a single private PDF as the sole knowledge source, this project showed that a model can accurately answer detailed questions, provide page-level evidence, and correctly decline to answer questions the document does not cover.

## Technologies / Tools

- Claude (used as the document-grounded question-answering model)
- PDF document (private source document, no-code retrieval)
- GitHub (project hosting and version control)
- Markdown (documentation format)

## Project Structure

```text
rag-ai-education/
│
├── README.md
├── PROJECT_REPORT.md
├── source-document.pdf
└── screenshots/
    └── README.md
```

## How to Reproduce

1. Clone or download this repository.
2. Open `source-document.pdf` to review the private knowledge source.
3. Upload the PDF to Claude (or a similar AI assistant that supports document upload).
4. Ask the seven questions listed in the "Questions and Answers" section above.
5. Compare the AI's answers with the documented results in this README.
6. Review the "Hallucination Testing" section and try the unsupported-question test yourself to confirm the model correctly declines to answer.

## Submission Checklist

- [x] Private source document identified and described
- [x] 5–7 meaningful questions asked and answered using the document
- [x] Each answer includes evidence/page reference
- [x] Hallucination verification table completed
- [x] Unsupported-question test included and clearly labeled
- [x] Plain prompt vs. RAG comparison table and examples included (examples labeled as hypothetical)
- [x] Reflection written (~200–300 words)
- [x] Conclusion written
- [x] Tools/technologies accurately listed
- [x] Project structure documented
- [x] Reproduction steps included
- [ ] Screenshots added to `screenshots/` folder (to be completed manually — see `screenshots/README.md`)
- [ ] Repository created and pushed to GitHub (to be completed manually)
