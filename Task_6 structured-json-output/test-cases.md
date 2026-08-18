# Test Cases

Five distinct customer support messages were used to test the prompt. Each
represents a different `issue_type` category. All expected outputs below are
**manually constructed / simulated** — they represent the correct target
output for a well-behaved model following `prompt.md`, not the output of an
actual API call.

---

### Test 1 — Payment Problem

**Input:**
```
Hi, my name is Sarah Collins. I was charged twice for my subscription this
month. My email is sarah.collins@email.com. Please refund the duplicate
charge as soon as possible, this is really frustrating.
```

**Expected JSON:**
```json
{
  "name": "Sarah Collins",
  "email": "sarah.collins@email.com",
  "issue_type": "payment",
  "urgency": "high",
  "message": "Customer was charged twice for their subscription this month and is requesting a refund of the duplicate charge as soon as possible."
}
```

**Validation:** Valid JSON, all five required keys present, `issue_type` is
a valid enum value ("payment"), `urgency` is a valid enum value ("high",
justified by "as soon as possible" and frustrated tone), name and email are
taken directly from the message with nothing invented.

---

### Test 2 — Account Problem

**Input:**
```
I can't log into my account anymore, it keeps saying my password is wrong
even after I reset it. Can someone help? My name's Daniel Osei.
```

**Expected JSON:**
```json
{
  "name": "Daniel Osei",
  "email": "",
  "issue_type": "account",
  "urgency": "medium",
  "message": "Customer cannot log into their account; the system says the password is incorrect even after a password reset."
}
```

**Validation:** Valid JSON, matches schema. `email` correctly defaults to an
empty string since none was given (no fabricated email). `issue_type` is
"account". `urgency` is "medium" — a real access problem but no explicit
urgent language or account-security threat language was used.

---

### Test 3 — Technical Problem

**Input:**
```
The mobile app crashes every time I try to upload a photo to my profile.
I'm using an Android phone. This has been happening for the past week.
Email: d.osei99@mailbox.com
```

**Expected JSON:**
```json
{
  "name": "",
  "email": "d.osei99@mailbox.com",
  "issue_type": "technical",
  "urgency": "medium",
  "message": "The mobile app crashes every time the customer tries to upload a profile photo on Android. The issue has been occurring for about a week."
}
```

**Validation:** Valid JSON, matches schema. `name` correctly left empty since
no name was stated (this is a different, unrelated customer from Test 2,
despite the similar email domain style — no assumption is made that it's the
same person). `issue_type` is "technical". `urgency` is "medium" since it is
disruptive but not blocking account access or payments.

---

### Test 4 — Delivery Problem

**Input:**
```
Order #58291 was supposed to arrive last Tuesday and it still hasn't shown
up. Tracking hasn't updated in 5 days. My name is Priya Nair,
priya.nair@shopmail.com. This is time-sensitive, it's a birthday gift and
the birthday is tomorrow!
```

**Expected JSON:**
```json
{
  "name": "Priya Nair",
  "email": "priya.nair@shopmail.com",
  "issue_type": "delivery",
  "urgency": "high",
  "message": "Order #58291 has not arrived; it was expected last Tuesday and tracking has not updated in 5 days. The customer needs it urgently as it is a birthday gift needed by tomorrow."
}
```

**Validation:** Valid JSON, matches schema. `issue_type` is "delivery".
`urgency` is "high" due to the explicit time constraint ("tomorrow") stated
by the customer, not just inferred tone. Order number is preserved inside
`message` since the schema has no dedicated field for it.

---

### Test 5 — Refund Problem

**Input:**
```
I returned my order two weeks ago (return label RL-4471) but I still
haven't received my refund. Could you check on this when you get a chance?
No rush, just following up. — Michael Chen, m.chen@inboxmail.com
```

**Expected JSON:**
```json
{
  "name": "Michael Chen",
  "email": "m.chen@inboxmail.com",
  "issue_type": "refund",
  "urgency": "low",
  "message": "Customer returned their order two weeks ago (return label RL-4471) but has not yet received the refund. They are following up and stated there is no rush."
}
```

**Validation:** Valid JSON, matches schema. `issue_type` is "refund".
`urgency` is "low" because the customer explicitly says "no rush," which
under the prompt's tie-breaking rule overrides any inferred urgency from the
delay itself.
