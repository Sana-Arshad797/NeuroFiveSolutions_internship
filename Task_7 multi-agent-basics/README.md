# Multi-Agent Basics — Two AIs Working Together

A small, beginner-friendly Python project that demonstrates **multi-agent
orchestration** using two specialized AI agents that work together in a
sequential pipeline: a **Writer Agent** drafts content on a topic, and an
**Editor/Critic Agent** reviews and improves that draft.

This project satisfies the "Multi-Agent Basics" assignment (Week 4:
Generative AI & Prompt Engineering) by building the pipeline manually with
two chained OpenAI API calls — **no LangChain or other agent framework is
used.**

---

## 1. What This Project Does

You give it a topic. Two AI "agents" — each with its own persona, job, and
system prompt — work on it one after another:

1. **Agent 1 (Writer)** reads the topic and writes a first draft.
2. **Agent 2 (Editor/Critic)** reads *that exact draft* (not the original
   topic alone) and rewrites it into an improved final version, along with
   a list of what it changed.

The program runs this pipeline automatically on two required demo topics,
then lets you try your own topic too.

---

## 2. Multi-Agent Architecture Explained

"Multi-agent" simply means more than one AI, each with a distinct role,
working together toward a shared goal — where one agent's output becomes
another agent's input. That hand-off is what makes it a *pipeline* rather
than two unrelated AI calls.

In this project:

- **Agent 1 — Writer** (`agents/writer.py`): Only responsible for drafting.
  It has no idea an Editor Agent even exists.
- **Agent 2 — Editor/Critic** (`agents/editor.py`): Only responsible for
  reviewing and improving. It is explicitly given Agent 1's raw draft as
  part of its prompt, and is instructed to preserve the original intent
  while fixing weaknesses.

Because Agent 2's prompt literally contains Agent 1's generated text, this
is a genuine two-agent pipeline, not two independent, unrelated API calls
generating separate content.

### Architecture Diagram

```
User Topic
    |
    v
Writer Agent (API Call #1)
    |
    v
Raw Draft
    |
    v
Editor/Critic Agent (API Call #2)
    |
    v
Final Draft + Improvement Notes
```

This is a **sequential two-agent pipeline**: Agent 2 does not run until
Agent 1 has finished, and Agent 2 receives Agent 1's actual generated
output as input — it is passed directly into the second API call.

---

## 3. Technologies Used

- Python 3
- [OpenAI Python SDK](https://github.com/openai/openai-python) (current,
  non-deprecated `client.chat.completions.create(...)` syntax)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) for loading
  the API key from a local `.env` file
- No LangChain, no databases, no web frameworks, no Docker — kept
  intentionally simple.

---

## 4. Project Structure

```
multi-agent-basics/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py
├── agents/
│   ├── __init__.py
│   ├── writer.py       # Agent 1: Writer
│   └── editor.py       # Agent 2: Editor/Critic
├── outputs/
│   ├── topic1_result.md
│   └── topic2_result.md
└── docs/
    └── assignment-notes.md
```

---

## 5. Installation Instructions

### Step 1 — Get the code

Clone the repository (or download/unzip the project folder), then move
into it:

```bash
cd multi-agent-basics
```

### Step 2 — (Recommended) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Creating and Configuring Your `.env` File

Your API key must **never** be hardcoded or committed to GitHub. Instead:

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in a text editor and replace the placeholder with your real
   OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-real-key-here
   ```
3. Save the file. `.gitignore` already excludes `.env` from Git, so it
   will never be uploaded.

---

## 7. How to Run the Project

```bash
python main.py
```

The program will:

1. Load your API key from `.env`.
2. Automatically run the full pipeline on both demo topics.
3. Print the raw draft, final draft, and improvement notes for each topic.
4. Save each result into `outputs/topic1_result.md` and
   `outputs/topic2_result.md`.
5. Ask if you'd like to try your own topic.

---

## 8. How the Two API Calls Work

**API Call #1 — Writer Agent** (`agents/writer.py`, function
`generate_draft()`):

```python
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": WRITER_SYSTEM_PROMPT},
        {"role": "user", "content": f"Write a draft about: {topic}"},
    ],
)
```

This call only knows about the topic. Its output is stored in a variable
called `raw_draft` inside `main.py`.

**API Call #2 — Editor Agent** (`agents/editor.py`, function
`edit_draft()`):

```python
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": EDITOR_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},  # includes raw_draft
    ],
)
```

`user_message` embeds `raw_draft` directly inside the prompt text, so the
Editor Agent is literally reviewing the Writer Agent's real output.

---

## 9. How Agent 1's Output Becomes Agent 2's Input

In `main.py`, the function `run_pipeline()` does this hand-off explicitly:

```python
raw_draft = generate_draft(client, topic)        # Agent 1 runs first
editor_output = edit_draft(client, topic, raw_draft)  # raw_draft passed to Agent 2
```

`raw_draft` is the actual string returned by the Writer Agent's API call.
It is passed as an argument into `edit_draft()`, which embeds it inside
the Editor Agent's prompt. There is no faking or generating both outputs
independently — Agent 2 cannot run without Agent 1's result.

---

## 10. Demo Topics

The pipeline runs automatically on these two required topics:

1. **"The Importance of Cybersecurity in Artificial Intelligence"**
2. **"Why Strong Passwords Are Important for Online Security"**

You can also enter a third, custom topic when prompted after the demo
runs.

---

## 11. Example Output

```
==================================================
MULTI-AGENT CONTENT PIPELINE
==================================================

TOPIC 1: The Importance of Cybersecurity in Artificial Intelligence

---------------- AGENT 1: WRITER ----------------
[raw draft text here]

---------------- AGENT 2: EDITOR ----------------
[final improved draft text here]

------------- EDITOR IMPROVEMENTS ---------------
- Removed repeated sentences
- Improved sentence flow and structure
- Clarified vague statements
- Strengthened the conclusion
==================================================
```

See `outputs/topic1_result.md` and `outputs/topic2_result.md` for full
worked examples (clearly marked as illustrative — see Section 15 below).

---

## 12. What the Editor Agent Typically Improves

Across both demo runs, the Editor Agent consistently:

- **Removes repetition** — filler sentences that repeat a point already
  made (e.g., "Passwords are important") are cut.
- **Improves sentence flow** — short, choppy sentences are combined into
  smoother, more readable ones.
- **Clarifies vague statements** — generic claims are made specific and
  concrete.
- **Strengthens weak explanations/conclusions** — endings are rewritten
  to state a clear takeaway instead of a generic summary.
- **Tightens overall structure** — ideas are reordered or connected more
  logically where needed.

Because the actual improvements depend on the live model's output, the
exact list will vary slightly each time you run the program — but the
*categories* above are what the Editor Agent is prompted to check for.

---

## 13. Security Note — Protecting Your API Key

**Never upload your real API key to GitHub.** If a key is exposed
publicly:

- Anyone can use it to make API calls billed to your account.
- OpenAI or GitHub's automated secret-scanning may revoke it.
- It can be hard to know how much unauthorized usage occurred before you
  notice.

This project protects your key by:

- Loading it only from a local `.env` file via `python-dotenv`.
- Never printing the key or hardcoding it anywhere in the code.
- Excluding `.env` from Git via `.gitignore`.
- Providing `.env.example` (with a placeholder, not a real key) so
  others know what variable to set.

If you ever accidentally commit a real key, **revoke/rotate it
immediately** in your OpenAI account dashboard, even if you remove it
from the code afterward.

---

## 14. Troubleshooting

**"ERROR: OPENAI_API_KEY was not found."**
You haven't created a `.env` file yet, or it's missing the key. Copy
`.env.example` to `.env` and add your real key (see Section 6).

**`ModuleNotFoundError: No module named 'openai'` (or `dotenv`)**
Your dependencies aren't installed. Run:
```bash
pip install -r requirements.txt
```
Make sure your virtual environment is activated first, if you're using
one.

**`AuthenticationError` from the OpenAI API**
Your API key is invalid, expired, or mistyped in `.env`. Double-check it
against your OpenAI account dashboard.

**`RateLimitError` or quota errors**
Your OpenAI account has hit its usage limit or has no billing set up.
Check your usage/billing page on the OpenAI platform.

**Import errors when running `main.py`**
Make sure you're running the program from the project's root folder
(the one containing `main.py`), not from inside `agents/`:
```bash
cd multi-agent-basics
python main.py
```

---

## 15. Assignment Requirements Checklist

| Requirement | Status | Where it's implemented |
|---|---|---|
| Design a 2-agent pipeline | ✅ | `agents/writer.py` (Agent 1), `agents/editor.py` (Agent 2) |
| Agent 1 = Writer drafts content | ✅ | `generate_draft()` in `agents/writer.py` |
| Agent 2 = Editor reviews/improves Agent 1's draft | ✅ | `edit_draft()` in `agents/editor.py` |
| Built manually by chaining two API calls (no LangChain) | ✅ | `run_pipeline()` in `main.py` calls both agents sequentially |
| Distinct system prompt/persona per agent | ✅ | `WRITER_SYSTEM_PROMPT`, `EDITOR_SYSTEM_PROMPT` |
| Run on 2 different topics | ✅ | `DEMO_TOPICS` list in `main.py`, run automatically |
| Compare final output vs raw Agent 1 draft | ✅ | Both are printed and saved side-by-side in the terminal and in `outputs/*.md` |
| Note what the Editor actually improved | ✅ | Editor Agent returns an "IMPROVEMENTS" section, displayed and saved separately |
| Agent 2 must receive Agent 1's real output | ✅ | `raw_draft` is passed directly into `edit_draft()` |
| Python 3 + official OpenAI SDK | ✅ | `requirements.txt`, `client.chat.completions.create(...)` syntax |
| No LangChain / unnecessary frameworks | ✅ | Only `openai` and `python-dotenv` are used |
| API key via environment variables, never hardcoded | ✅ | `.env` + `python-dotenv`, `.gitignore` excludes `.env` |
| Handle missing API key / API errors gracefully | ✅ | `get_client()` and `run_pipeline()` in `main.py` |

---

## Note on the `outputs/` Files

`outputs/topic1_result.md` and `outputs/topic2_result.md` currently
contain **hand-written example results**, clearly labeled as such at the
top of each file. They show what the program's real output looks like,
but they were not produced by a live API call. Running `python main.py`
with a valid API key will overwrite them with real, model-generated
results.
