# Structured Outputs — Customer Support JSON Extraction

## Overview

LLMs naturally respond in free-form text, but most real applications —
ticketing systems, CRMs, dashboards, automated routing — need predictable,
machine-readable data. If an application has to parse a paragraph of prose
to figure out a customer's email or how urgent their issue is, the
integration becomes fragile and error-prone. Structured JSON output solves
this: instead of asking the model to "help," we ask it to fill in a fixed
data contract that our code can parse directly with `JSON.parse()`, no
regex or guesswork required.

## Objective

The goal of this project is to force a large language model to convert
messy, natural-language customer support messages into predictable JSON
that a downstream application can consume directly — with no manual
cleanup, no ambiguity, and no risk of the model inventing data that wasn't
actually provided by the customer.

## Use Case

**Customer Support Message → Structured JSON.** A support inbox receives
unstructured messages from customers (emails, contact-form submissions,
chat messages). Instead of a human manually tagging each message with a
category and urgency level, an LLM reads the raw message and extracts a
structured record that could be inserted straight into a ticketing
database.

## JSON Schema

```json
{
  "name": "string",
  "email": "string",
  "issue_type": "string",
  "urgency": "string",
  "message": "string"
}
```

Field explanations:

- **name** — The customer's name, exactly as stated in their message.
  Empty string if not provided.
- **email** — The customer's email address, exactly as stated. Empty string
  if not provided. Never auto-corrected or guessed.
- **issue_type** — One of a fixed set of categories: `payment`, `account`,
  `technical`, `delivery`, `refund`, `other`. Keeping this as a closed enum
  (rather than free text) means downstream code can safely route tickets
  with a simple switch statement.
- **urgency** — One of `low`, `medium`, `high`, inferred from the content
  and tone of the message, with explicit customer statements about urgency
  taking priority over inferred tone.
- **message** — The customer's actual problem, preserved faithfully (light
  grammar cleanup allowed, but no new information added).

The full formal definition, including enum constraints and
`additionalProperties: false`, is in [`schema.json`](./schema.json).

## Prompt Constraints

The production prompt (see [`prompt.md`](./prompt.md)) requires the model
to:

- Return **JSON only** — nothing else.
- Return **no Markdown**, including no ` ```json ` code fences.
- Return **no explanations** before or after the JSON.
- Follow the **exact schema** with exactly five keys.
- Return **valid, parseable JSON** every time.
- Use only the **allowed enum values** for `issue_type` and `urgency`.
- **Never invent** a name, email, or detail not present in the message —
  missing information is represented with a safe empty-string or "other"
  default instead of a guess.

## Testing

The prompt was tested on 5 different sample customer messages, covering a
payment issue, an account issue, a technical issue, a delivery issue, and a
refund issue. Full inputs and expected outputs are in
[`test-cases.md`](./test-cases.md). All five expected outputs were checked
programmatically and confirmed to be valid JSON that conforms to
`schema.json`.

## Break Test

A single deliberately messy, contradictory customer message was used to
stress-test the prompt: it included typos, two possible emails, two
unrelated problems in one message, and directly conflicting urgency signals
("ASAP" vs. "no rush"). Full details are in [`results.md`](./results.md).

## Prompt Improvement

An earlier, simpler baseline prompt still produced valid JSON on the tricky
input, but left three things underspecified: which email to use when two
are given, which issue to treat as primary when two are mentioned, and how
to resolve contradictory urgency language. The final prompt in
`prompt.md` adds explicit rules for all three cases so the output is
deterministic instead of a coin flip. See the **Prompt Fix** section of
`results.md` for the full before/after comparison.

## Results

| Test | Input Type | JSON Valid? | Schema Valid? |
|------|------------|-------------|----------------|
| 1 | Payment | Yes | Yes |
| 2 | Account | Yes | Yes |
| 3 | Technical | Yes | Yes |
| 4 | Delivery | Yes | Yes |
| 5 | Refund | Yes | Yes |
| Break test (baseline prompt) | Messy/contradictory | Yes | Yes (but non-deterministic behavior) |
| Break test (improved prompt) | Messy/contradictory | Yes | Yes (deterministic, no invented data) |

Full detail, including the exact JSON for every test, is in
[`results.md`](./results.md).

## Lessons Learned

Strict schemas and explicit constraints matter more than they first appear
to. A prompt can produce technically valid JSON while still being
unreliable in the ways that matter for a real application — inconsistent
category choices, guessed contact information, or unpredictable
tie-breaking on ambiguous input. Structured output isn't just "ask for
JSON"; it's about writing rules precise enough that the model's behavior
is the same on every run, especially on messy, real-world input. This is
exactly what makes structured output usable for APIs, database inserts, and
automated pipelines instead of just being convenient for human reading.

## Project Structure

```text
structured-json-output/
│
├── README.md
├── schema.json
├── prompt.md
├── test-cases.md
├── results.md
└── examples/
    └── sample-output.json
```

## How to Use

1. Open [`schema.json`](./schema.json) to see the exact data contract the
   output must follow.
2. Copy the final prompt from [`prompt.md`](./prompt.md).
3. Paste it into your LLM of choice, replacing `{{CUSTOMER_MESSAGE}}` with a
   real customer support message.
4. Take the returned text and pass it directly to `JSON.parse()` (or your
   language's equivalent) — it should parse with no cleanup needed.
5. Validate the parsed object against `schema.json` using a JSON Schema
   validator (e.g. the `jsonschema` Python package or `ajv` in JavaScript)
   to confirm it's both syntactically and semantically correct.

## Conclusion

This project demonstrates a complete, practical workflow for structured
LLM output: designing a schema, writing a prompt that enforces it,
validating the result on multiple realistic inputs, deliberately trying to
break it, and improving the prompt based on what the break test revealed.
The result is a prompt that reliably turns messy customer messages into
clean, predictable JSON that a real application could use as-is.
