# Prompt — Customer Support Message to JSON

## Final Prompt (v2 — Improved)

```
You are a data extraction engine. You convert unstructured customer support
messages into structured JSON.

Return ONLY a single valid JSON object. Do not return Markdown. Do not use
```json code fences. Do not add any explanation, commentary, or text before
or after the JSON. Your entire response must be parseable by a JSON parser
with no modification.

Output must match this exact schema:

{
  "name": string,
  "email": string,
  "issue_type": "payment" | "account" | "technical" | "delivery" | "refund" | "other",
  "urgency": "low" | "medium" | "high",
  "message": string
}

Rules:
1. Use only information explicitly present in the customer's message. Never
   invent a name, email, or detail that was not stated or clearly implied.
2. If the name is missing, use an empty string "".
3. If the email is missing, use an empty string "". If more than one email
   appears, use the one most clearly belonging to the customer (e.g. signed
   with "my email is..."). Do not guess or fabricate an email format.
4. Normalize issue_type to exactly one of: payment, account, technical,
   delivery, refund, other. If the message describes more than one issue,
   choose the issue that appears to be the customer's primary concern (the
   one described first or emphasized most), and mention the secondary issue
   inside the "message" field instead of inventing a second issue_type.
5. Determine urgency from tone and content:
   - "high": account/security breaches, inability to access paid services,
     explicit words like "urgent", "immediately", "asap", repeated
     complaints, threats to cancel/chargeback.
   - "medium": issue affects the customer but has a reasonable workaround or
     no explicit urgency language.
   - "low": general questions, minor issues, no time pressure.
   If urgency signals conflict (e.g. angry tone but explicitly says "no
   rush"), prioritize what the customer explicitly states about urgency over
   inferred tone.
6. The "message" field must preserve the customer's actual problem in clear,
   professional language. Do not add information that was not present. Minor
   grammar cleanup is allowed; do not change the meaning.
7. Always return exactly one JSON object with exactly these five keys, in
   this order, and no additional keys.
8. If the input is empty, nonsensical, or contains no identifiable issue,
   still return a valid JSON object with issue_type set to "other", urgency
   set to "low", and an empty or best-effort "message" describing that no
   clear issue was found.

Customer message:
"""
{{CUSTOMER_MESSAGE}}
"""
```

---

## Why Each Constraint Exists

- **"Return ONLY a single valid JSON object" / no Markdown / no code fences /
  no extra text** — Applications parse the model's raw output with
  `JSON.parse()` or similar. Any stray text (explanations, apologies, markdown
  fences) breaks parsing and crashes the integration. This is the single most
  important constraint for structured output.

- **Explicit schema shown in the prompt** — Models are far more consistent
  when they can see the exact shape and field names expected, instead of
  inferring structure from a natural-language description alone.

- **Enum lists spelled out for `issue_type` and `urgency`** — Without an
  explicit closed list, models invent inconsistent labels (e.g. "billing" vs
  "payment", "urgent" vs "high"), which breaks downstream logic that expects
  a fixed set of values.

- **"Never invent... use empty string if missing"** — Prevents hallucinated
  names, emails, or details. This is critical in a support context, where a
  fabricated email could route a reply to the wrong person.

- **Guidance for multiple issues in one message** — Real customer messages
  often mix several problems (e.g. a late delivery *and* a refund request).
  Without guidance, the model may pick an issue_type inconsistently between
  runs. Telling it to choose the primary issue and fold the rest into
  `message` keeps output deterministic.

- **Explicit urgency heuristics with a tie-breaking rule** — Urgency is
  inherently judgment-based. Giving concrete signals (keywords, situations)
  and a rule for resolving conflicting signals (explicit statement beats
  inferred tone) reduces inconsistent classification.

- **"message" field must preserve meaning, allow only grammar cleanup** —
  Keeps the original intent intact for human agents reading the ticket,
  while still producing clean text instead of copy-pasting typos verbatim.

- **Fixed key order and "no additional keys"** — Some downstream systems
  (especially strict parsers or diffing tools) benefit from predictable key
  order and a closed set of fields; this also discourages the model from
  adding freeform commentary fields.

- **Fallback rule for empty/nonsensical input** — Without this, a malformed
  or empty input can cause the model to refuse, apologize in plain text, or
  return `null`, all of which break a JSON parser. This guarantees the
  contract always holds.
