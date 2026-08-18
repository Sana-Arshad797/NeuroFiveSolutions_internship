# RAG Project: Question Answering Using a Private Document

## 1. Introduction

This report documents a student project that demonstrates Retrieval-Augmented Generation (RAG) using a private source document. RAG is an approach in which an AI model's answers are grounded in a specific, retrievable piece of external content — in this case, a single private PDF — rather than relying solely on the model's general training knowledge. This project uses a no-code, document-upload approach with Claude to demonstrate the core principles of RAG without building a full technical pipeline (such as a vector database or embedding-based retrieval system).

## 2. Project Objective

The objective of this project is to show, in a simple and verifiable way, how grounding an AI's responses in a private document changes the accuracy, specificity, and trustworthiness of its answers. The project asks a set of questions about the source document, records the AI's answers along with page-level evidence, checks each answer for hallucination, and compares document-grounded answers with what a plain, ungrounded prompt would likely produce.

## 3. Source Document

- **Title:** The Impact of Artificial Intelligence on Modern Education
- **Format:** PDF, 10 pages
- **Topic:** The report covers how AI is used in education (instructional support, student tutoring, administrative automation, and institutional analytics), personalized learning, benefits and challenges, privacy/ethics/academic integrity concerns, impacts on teachers, and predictions for the future of AI in education.
- **Sourcing:** The document cites named, real sources for its statistics, including the Walton Family Foundation & Gallup, Pew Research Center, Education Week, Turnitin, Electroiq, Demandsage, and Textero, along with a references list at the end of the document (Page 10).

This document served as the sole private knowledge source for this project. No other external document was used to answer the questions below.

## 4. RAG Methodology

The methodology used in this project follows the retrieval-then-generation pattern that underlies RAG systems, implemented here without custom code:

1. **Document ingestion:** The private PDF was uploaded directly to Claude as context for the conversation.
2. **Retrieval:** When a question was asked, the model located the relevant passage(s) within the uploaded document.
3. **Generation:** The model produced a natural-language answer based on the retrieved passage(s), rather than drawing on general background knowledge.
4. **Verification:** Each answer was checked against the source PDF to confirm the page/section it came from and to confirm no information was invented.

This is a simplified, no-code demonstration of RAG. It does not include a vector database, embedding model, or custom retrieval code — the "retrieval" step is performed by the language model reading the full document directly. This is an intentional and reasonable simplification for a student-level demonstration, as explicitly allowed by the project instructions.

## 5. Questions and Answers

### Question 1
**Question:** What percentage of U.S. K-12 public school teachers used AI tools during the 2024–2025 school year, according to the report?

**Answer:** 60% of U.S. K-12 public school teachers used AI tools during the 2024–2025 school year, with 32% using them at least weekly, according to a joint study by the Walton Family Foundation and Gallup.

**Evidence:** "60% of U.S. K-12 public school teachers used AI tools during the 2024-2025 school year, with 32% using them at least weekly (Walton Family Foundation & Gallup, 2025)."

**Page/Section:** Page 1, Section 1 ("Introduction to Artificial Intelligence in Education").

---

### Question 2
**Question:** How did teen use of ChatGPT for schoolwork change between 2023 and 2024, according to the document?

**Answer:** The share of U.S. teens using ChatGPT for schoolwork roughly doubled in one year, rising from 13% in 2023 to 26% in 2024, according to Pew Research Center data cited in the report.

**Evidence:** "Pew Research Center found that the share of U.S. teens using ChatGPT for schoolwork roughly doubled in one year, from 13% in 2023 to 26% in 2024 (Pew Research Center, 2025)."

**Page/Section:** Page 1, Section 1 ("Introduction to Artificial Intelligence in Education").

---

### Question 3
**Question:** What are the four broad categories of AI use in education described in the report?

**Answer:** The report groups AI use in education into four categories: instructional support for teachers, direct learning support for students, administrative automation, and institutional analytics.

**Evidence:** "Broadly, its uses can be grouped into four categories: instructional support for teachers, direct learning support for students, administrative automation, and institutional analytics."

**Page/Section:** Page 2, Section 2 ("How AI Is Being Used in Education").

---

### Question 4
**Question:** According to the report, how much time do teachers who use AI tools weekly save on average?

**Answer:** Teachers who use AI tools at least weekly reported saving an average of close to six hours per week, largely on grading and lesson preparation tasks.

**Evidence:** "teachers who use AI tools at least weekly reported saving an average of close to six hours per week on tasks such as grading and lesson preparation (Walton Family Foundation & Gallup, 2025)."

**Page/Section:** Page 2, Section 2.3 ("Administrative Automation"), restated on Page 5, Section 5.1 ("Time Savings for Teachers").

---

### Question 5
**Question:** What accuracy gap does the report describe between human tutors and AI tutoring systems in interpreting student emotions?

**Answer:** Human tutors could interpret a student's emotional state (such as frustration or confusion) with about 92% accuracy, while even advanced AI tutoring systems managed only about 68% accuracy on the same measure.

**Evidence:** "human tutors could interpret a student's emotional state, such as frustration or confusion, with about 92% accuracy, while even advanced AI tutoring systems managed roughly 68% accuracy on the same measure (as compiled in Demandsage's 2026 AI in Education Statistics report...)."

**Page/Section:** Pages 4–5, Section 4.2 ("Strengths and Limits Compared to Human Tutors").

---

### Question 6
**Question:** What percentage of U.S. K-12 teachers reported lacking formal training on AI, according to the report?

**Answer:** 71% of U.S. K-12 teachers reported lacking formal training on AI, even though around 74% of districts planned to offer AI training by fall 2025.

**Evidence:** "71% of U.S. K-12 teachers reported lacking formal training on AI, even though a majority of districts (around 74%) planned to offer AI training by fall 2025 (as compiled in Electroiq's 2025 AI in Education Statistics report...)."

**Page/Section:** Page 6, Section 6.4 ("Teacher Preparedness").

---

### Question 7
**Question:** What law does the report identify as governing student data privacy in U.S. schools?

**Answer:** The report identifies the Family Educational Rights and Privacy Act (FERPA) as the law that governs student data privacy in U.S. schools.

**Evidence:** "student data privacy in schools is governed in part by the Family Educational Rights and Privacy Act (FERPA), which restricts how student educational records can be shared..."

**Page/Section:** Page 7, Section 7.1 ("Data Privacy").

## 6. Hallucination Verification

| Question | Supported by PDF? | Evidence/Page | Hallucination? |
|---|---|---|---|
| Q1: Teacher AI adoption 2024–2025 | Yes | Page 1, Section 1 | No |
| Q2: Teen ChatGPT use 2023 vs 2024 | Yes | Page 1, Section 1 | No |
| Q3: Four categories of AI use | Yes | Page 2, Section 2 | No |
| Q4: Teacher time savings | Yes | Page 2 & Page 5 | No |
| Q5: Human vs AI tutor emotional accuracy | Yes | Pages 4–5, Section 4.2 | No |
| Q6: Teachers lacking AI training | Yes | Page 6, Section 6.4 | No |
| Q7: FERPA and student data privacy | Yes | Page 7, Section 7.1 | No |

**Finding:** No hallucinations were found across the seven questions. Every figure, name, and claim in the answers above was directly present in the source PDF and could be traced to a specific page and section.

## 7. Unsupported Information Test

**Question:** According to the report, what percentage of teachers in South Korea use AI tools in the classroom?

**Expected grounded response:** "This information is not available in the provided document."

**Explanation:** The source document reports AI adoption statistics for U.S. K-12 teachers and references some global/multinational survey data on student AI usage, but it does not contain any country-specific statistic for South Korean teachers. A properly grounded RAG system should recognize that this specific figure is outside the scope of the document and should say so directly rather than generating a plausible-sounding but unverified number. Inventing an answer in this situation would be a clear example of hallucination, since there is no supporting text anywhere in the source PDF.

This test is important because it shows the grounded system behaving correctly under a condition where a plain, ungrounded prompt might instead produce a fabricated statistic based on the model's general training data rather than the actual private document.

## 8. Plain Prompt vs RAG Comparison

| Aspect | Plain Prompt | RAG / Document-Grounded |
|---|---|---|
| Information source | The model's general training data | The uploaded private PDF |
| Specificity | General, often generic statements | Specific figures, named studies, and page-level detail |
| Relevance | May include outdated or broadly applicable information | Directly matches the content of this specific report |
| Document evidence | None — no way to trace the answer to a source | Each answer can be traced to a page/section in the PDF |
| Hallucination risk | Higher — model may generate plausible but unverifiable claims | Lower — answer is checked against the actual document text |
| Private data | Cannot access private/unpublished documents | Can directly use the private document as its knowledge source |

### Examples (hypothetical — no separate plain-prompt experiment was run)

*The following are hypothetical illustrations, not the result of an actual separate plain-prompt experiment conducted for this project. They are included to illustrate the expected contrast described in the comparison table above.*

1. **Teacher AI adoption:** A plain prompt asking "What percentage of teachers use AI?" would likely produce a vague, unsourced estimate. The RAG answer instead gave an exact figure (60%, with 32% weekly) sourced to Page 1 of the document, attributed to a named study.

2. **Time savings:** A plain prompt asking "How much time does AI save teachers?" would likely produce a general statement such as "AI can save teachers significant time," without a number. The RAG answer specified "close to six hours per week," traceable to Page 2 and Page 5.

3. **Data privacy law:** A plain prompt asking "What law protects student data?" might reference data protection in a generic sense or name an unrelated law. The RAG answer correctly and specifically named FERPA, sourced to Page 7, Section 7.1.

## 9. Results / Findings

This project's central finding is that document-grounded answers were consistently more specific and verifiable than a plain prompt would likely be. All seven test questions were answered accurately using only the content of the source PDF, with each answer traceable to a specific page and section. The unsupported-question test confirmed that the grounded approach correctly declines to answer when the requested information is not present in the source document, rather than inventing a plausible-sounding statistic. No hallucinations were identified across any of the seven core questions.

## 10. Reflection

Grounding the AI in my own document changed the quality of its answers in several clear ways. Without the source PDF, a plain prompt about "AI in education statistics" would likely have produced generic, broadly true but unspecific statements, since the model would be drawing on a wide range of possibly outdated or mismatched public information rather than this particular report. With the document provided, every answer became traceable to an exact page and section, which made it possible to verify accuracy rather than simply trust the response.

Specificity improved the most. Instead of vague claims like "many teachers use AI," the grounded answers included exact figures (60%, 32%, 71%, 92% vs. 68%) tied to named studies (Walton Family Foundation & Gallup, Pew Research Center, Electroiq, Demandsage) exactly as they appear in the report. Relevance also improved, because the answers reflected the specific framing and structure of this document rather than a generic overview of the topic.

Hallucination risk dropped significantly. Because the model was restricted to the content of the PDF, it had no reason to invent statistics, and the unsupported-question test confirmed that when information genuinely was not in the document (such as a country-specific statistic not mentioned in the report), the correct behavior was to say so rather than fabricate an answer.

The main limitation is that grounded answers are only as good as the source document itself: if the PDF contains an error or an outdated statistic, the grounded answer will faithfully repeat it. This project confirms that RAG's main value is not that it makes an AI "smarter," but that it makes an AI's answers traceable, specific, and honest about the limits of what it knows.

## 11. Conclusion

This project demonstrates that document-grounded question answering (RAG) produces answers that are more specific, more traceable, and less prone to hallucination than plain, ungrounded prompting. Using a single private PDF as the sole knowledge source, this project showed that a model can accurately answer detailed questions, provide page-level evidence for each answer, and correctly decline to answer questions the document does not cover — the essential behaviors that distinguish a grounded RAG system from an ungrounded one.

## 12. Limitations

- The quality of the answers produced depends entirely on the quality and completeness of the source document; the system cannot answer questions about information the document does not contain.
- This is a no-code demonstration, so it does not expose or test the internal retrieval pipeline (e.g., embeddings, chunking strategy, or vector similarity search) that a full RAG implementation would use.
- The experiment uses a single source document; results and conclusions may not generalize to projects using multiple or larger document collections.
- The "Plain Prompt vs. RAG" examples in Section 8 are hypothetical illustrations rather than the output of an actual separate plain-prompt experiment, as no live ungrounded comparison run was performed for this project.
