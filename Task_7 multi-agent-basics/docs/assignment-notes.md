# Assignment Notes — Requirement-to-Implementation Mapping

This document maps each requirement from the "Multi-Agent Basics — Two AIs
Working Together" assignment directly to where it's implemented in this
project

---

**Requirement:** Design a 2-agent pipeline.
**Implementation:** `agents/writer.py` and `agents/editor.py` implement
the two specialized agents. `main.py` wires them into a pipeline via the
`run_pipeline()` function.

---

**Requirement:** Agent 1 = Writer, drafts content on a given topic.
**Implementation:** `agents/writer.py` defines `WRITER_SYSTEM_PROMPT` and
the `generate_draft()` function, which makes the first API call using
only the topic as input.

---

**Requirement:** Agent 2 = Editor/Critic, reviews and improves Agent 1's
draft.
**Implementation:** `agents/editor.py` defines `EDITOR_SYSTEM_PROMPT` and
the `edit_draft()` function, which takes the topic *and* Agent 1's raw
draft as arguments and returns an improved draft plus improvement notes.

---

**Requirement:** Build it manually by chaining two API calls. Do NOT use
LangChain.
**Implementation:** `main.py`'s `run_pipeline()` calls `generate_draft()`
first, stores the result in `raw_draft`, then calls `edit_draft()` and
passes `raw_draft` directly in as a parameter. Both calls use the plain
`openai` Python SDK (`client.chat.completions.create(...)`) — no agent
framework is imported anywhere in the project.

---

**Requirement:** Give each agent a distinct system prompt/persona and
clear responsibilities.
**Implementation:** `WRITER_SYSTEM_PROMPT` (in `writer.py`) and
`EDITOR_SYSTEM_PROMPT` (in `editor.py`) are separate constants with
different instructions — one focused purely on drafting, the other purely
on reviewing/improving.

---

**Requirement:** Run the pipeline on 2 different topics.
**Implementation:** `DEMO_TOPICS` in `main.py` contains both required
topics. `main()` loops over them and runs the full pipeline on each
automatically, with no user interaction required.

---

**Requirement:** Compare the final post-Editor output with the raw Agent
1 draft.
**Implementation:** `display_result()` in `main.py` prints the raw draft
(`AGENT 1: WRITER` section) directly above the final draft (`AGENT 2:
EDITOR` section) for each topic, so they can be compared side by side.
The same structure is written to each file in `outputs/`.

---

**Requirement:** Clearly note what the Editor agent actually improved.
**Implementation:** The Editor Agent is explicitly instructed (in its
system prompt and in the user message built by `edit_draft()`) to end its
response with an "IMPROVEMENTS" section. `parse_editor_output()` in
`main.py` splits this out and displays/saves it separately under an
`EDITOR IMPROVEMENTS` heading.

---

**Requirement:** The second API call must actually receive Agent 1's
output — no faking multi-agent behavior.
**Implementation:** In `run_pipeline()`:
```python
raw_draft = generate_draft(client, topic)
editor_output = edit_draft(client, topic, raw_draft)
```
`raw_draft` is the literal return value of the first API call, passed as
an argument into the second. `edit_draft()` embeds this exact text inside
the Editor Agent's prompt (`agents/editor.py`), so the Editor is reviewing
real Writer output, not independently generated content.

---

## Why This Counts as Multi-Agent Orchestration Without LangChain

LangChain (and similar frameworks) provide pre-built abstractions for
chaining LLM calls, managing memory, and coordinating multiple "agents."
But the underlying concept of multi-agent orchestration doesn't require
a framework — it requires:

1. **Multiple distinct roles**, each with its own instructions/persona.
   ✅ Writer vs. Editor, defined by separate system prompts.
2. **A defined hand-off**, where one agent's output becomes another
   agent's input. ✅ `raw_draft` flows from Agent 1's return value into
   Agent 2's prompt.
3. **Sequential coordination**, where the second agent cannot run
   meaningfully until the first has produced its result. ✅ `edit_draft()`
   is only called after `generate_draft()` completes.

This project implements all three properties directly with plain Python
functions and two `client.chat.completions.create()` calls. LangChain
would offer higher-level abstractions (like a `Chain` or `Agent` class)
for the same pattern, but the core multi-agent behavior — distinct roles
working sequentially, with real data passed between them — is fully
present here without it.
