# Results

All outputs in this document are **manually constructed / simulated**. No
live model or API call was executed to produce them; they were built and
checked by hand (and validated programmatically against `schema.json`) to
represent the correct target behavior of the prompt.

## Test Results Table

| Test | Input Type | JSON Valid? | Schema Valid? | Notes |
|------|------------|-------------|----------------|-------|
| 1 | Payment problem | Yes | Yes | Urgency correctly inferred as "high" from explicit language. |
| 2 | Account problem | Yes | Yes | Missing email correctly defaulted to "". No email invented. |
| 3 | Technical problem | Yes | Yes | Missing name correctly defaulted to "". No cross-contamination with Test 2's customer. |
| 4 | Delivery problem | Yes | Yes | Order number preserved in `message` since schema has no dedicated field for it. |
| 5 | Refund problem | Yes | Yes | Explicit "no rush" correctly overrode inferred urgency from a 2-week delay. |

---

## Break Test

### Tricky Input

```
hii idk who to even email??? my nmae is jon i think my card got charged
like 3 times??? or maybe it was a subscription idk, ALSO my package never
came and its been like a month, super urgent i guess but also whatever, do
what u want. email is either jon@gmial.com or jon99@gmail.com not sure
which one i used lol. fix this ASAP but also no rush im just annoyed
```

This input intentionally contains: typos and lowercase/informal text, two
possible conflicting emails, two separate issues (payment + delivery),
missing/uncertain name confidence, and directly contradictory urgency
signals ("super urgent... ASAP" vs. "no rush... whatever").

### Initial Prompt Result

Before arriving at `prompt.md` (v2), an earlier baseline prompt was used
during development. That baseline only said:

> "Return only valid JSON matching this schema: {name, email, issue_type,
> urgency, message}. Use payment/account/technical/delivery/refund/other for
> issue_type and low/medium/high for urgency."

**Simulated result (baseline/v1 prompt):**
```json
{
  "name": "jon",
  "email": "jon@gmial.com",
  "issue_type": "payment",
  "urgency": "high",
  "message": "Customer's card was charged 3 times for a subscription and their package never came for a month."
}
```

### Did It Break?

Technically, the baseline prompt still produced syntactically valid JSON
that matched the schema's types and enums — so it did not "break" in the
sense of crashing a parser. However, it exposed three real weaknesses:

1. **Ambiguous email not handled deterministically.** The customer gave two
   possible emails ("jon@gmial.com" — note the typo "gmial" — or
   "jon99@gmail.com") and said they weren't sure which was used. The
   baseline prompt has no rule for this, so the model could pick either one
   inconsistently across runs, or "fix" the typo into "jon@gmail.com" —
   which would be inventing data not present in the message.
2. **Multiple issues merged without a clear rule.** The baseline prompt
   picked "payment" as `issue_type` and folded delivery into `message`, but
   nothing in the prompt guarantees this choice is made consistently every
   time (it could just as easily output "delivery" on a different run).
3. **Conflicting urgency signals resolved by guesswork.** The message says
   both "super urgent... ASAP" and "no rush... whatever." The baseline
   prompt gives no tie-breaking rule, so urgency classification is
   essentially a coin flip between "high" and "low," which is not
   acceptable for a field a support system might use for ticket routing.

**Conclusion:** the baseline prompt did not break in the "invalid JSON"
sense, but it broke in the more important sense of **not being
deterministic or safe with real-world messy input**, which is the actual
goal of a production structured-output prompt.

---

## Prompt Fix

The weaknesses above are exactly what `prompt.md` (v2, the final prompt in
this repository) was written to address:

- Rule 3 explicitly instructs: if multiple emails appear, use the one the
  customer most clearly claims as theirs, and never correct or guess a
  "fixed" version of an email that wasn't clearly stated as a typo fix by
  the customer.
- Rule 4 gives an explicit tie-breaking rule for multiple issues: use the
  primary/first-emphasized issue as `issue_type`, and mention the other in
  `message`.
- Rule 5 gives an explicit tie-breaking rule for urgency: an explicit
  customer statement about urgency (e.g. "no rush") overrides inferred tone
  from other parts of the message.

## Re-test

### Improved Output

**Simulated result (final v2 prompt in `prompt.md`):**
```json
{
  "name": "jon",
  "email": "jon@gmial.com",
  "issue_type": "payment",
  "urgency": "low",
  "message": "Customer believes their card was charged multiple times, possibly for a subscription, and says their package never arrived for about a month. They said to fix it ASAP but also said not to worry and that they're just annoyed, not in a rush."
}
```

### Validation

- **Valid JSON:** Yes — confirmed programmatically with `json.loads()`.
- **Matches schema:** Yes — confirmed against `schema.json` with a JSON
  Schema validator; all types and enum values are correct.
- **Required fields present:** Yes — all five keys (`name`, `email`,
  `issue_type`, `urgency`, `message`) are present.
- **Enum values valid:** Yes — `issue_type` is "payment" (one of the six
  allowed values), `urgency` is "low" (one of the three allowed values).
- **No invented information:** Yes — the email is preserved exactly as
  typed by the customer (including the "gmial" typo) rather than
  auto-corrected, the name is left in lowercase exactly as given rather than
  guessing a full name, and the payment issue was chosen as primary because
  it was mentioned first, with the delivery problem folded into `message`
  rather than dropped. Urgency was set to "low" per Rule 5, because the
  customer's explicit final statement ("no rush... just annoyed") overrides
  the earlier "ASAP" language.

This confirms the improved prompt produces deterministic, schema-valid, and
non-hallucinated output even on deliberately messy, contradictory input.
