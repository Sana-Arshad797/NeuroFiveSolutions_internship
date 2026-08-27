# Manual Test Cases

These test cases are meant to be run manually through the web interface
(or via `curl`/Postman against `POST /api/analyze`) to demonstrate that the
application behaves correctly across a range of realistic inputs.

Because the AI model's exact wording will vary between runs, these test
cases describe the **expected type of result** and **what each test
demonstrates**, rather than an exact expected output.

---

## Test Case 1: Multiple Failed Login Attempts

**Input:**
```
Multiple failed login attempts (12) for user 'jsmith' from IP 203.0.113.45
within a 3-minute window, followed by one successful login at 09:41 UTC
from the same IP address.
```

**Expected type of result:**
- `threat_type` referencing brute force / credential access or account
  compromise.
- `severity` of Medium or High, since a successful login followed the
  failed attempts.
- `indicators` should include the username `jsmith`, the IP
  `203.0.113.45`, and the attempt count/timeframe.
- `recommended_actions` should include things like resetting the
  password, reviewing the account's recent activity, and enabling MFA.

**What this demonstrates:**
- The system prompt correctly identifies brute-force patterns.
- Indicator extraction pulls concrete values directly from the input.
- Severity scaling reflects the presence of a successful login after
  failures (higher risk than failures alone).

---

## Test Case 2: Suspicious PowerShell Activity

**Input:**
```
Endpoint detection alert: powershell.exe was launched by winword.exe on
host FIN-LAPTOP-07 at 14:32 UTC. The PowerShell command line was
base64-encoded and included the flag '-enc'. The process then attempted
an outbound HTTPS connection to an IP address not previously seen on this
host.
```

**Expected type of result:**
- `threat_type` referencing malicious script execution, living-off-the-land
  techniques, or possible malware/macro-based attack.
- `severity` of High, since Office spawning PowerShell with an
  encoded command is a well-known suspicious pattern.
- `indicators` should include `powershell.exe`, `winword.exe`,
  `FIN-LAPTOP-07`, and the `-enc` flag.
- `recommended_actions` should include isolating the host and
  investigating the parent process chain.

**What this demonstrates:**
- The model can reason about process relationships (parent/child) that
  are commonly used in real EDR-style detections.
- Recommendations are practical and defender-focused, not generic.

---

## Test Case 3: Unusual Outbound Network Connection

**Input:**
```
Firewall log: internal host 10.0.14.22 established an outbound connection
on port 4444 to external IP 198.51.100.77 lasting 45 minutes. This port
and destination have not been seen in the last 30 days of traffic for
this host.
```

**Expected type of result:**
- `threat_type` referencing possible command-and-control (C2) activity,
  given port 4444 is commonly associated with reverse shells/C2 tools.
- `severity` of Medium to High depending on how the model weighs a single
  unusual connection.
- `indicators` should include the internal IP, external IP, and port.
- `recommended_actions` should include blocking/monitoring the
  destination and reviewing the host for compromise.

**What this demonstrates:**
- The model can flag anomalous network behavior based on
  baseline-deviation language ("not seen in the last 30 days").
- Shows the tool's value for log/traffic-based alerts, not just
  endpoint alerts.

---

## Test Case 4: Malware Detection Alert

**Input:**
```
Antivirus alert: file 'invoice_2024.exe' was detected and quarantined on
host ACCT-PC-03. Signature match: Trojan.GenericKD. The file was
downloaded via a browser from an email link received 10 minutes prior to
detection.
```

**Expected type of result:**
- `threat_type` referencing malware/trojan delivered via phishing.
- `severity` of High, since malware was confirmed by signature match,
  though it was quarantined (reducing but not eliminating impact).
- `indicators` should include the filename, host, and signature name.
- `recommended_actions` should include verifying quarantine success,
  scanning the host, and checking for the phishing email
  across other mailboxes.

**What this demonstrates:**
- The application handles alerts that include a confirmed detection
  (not just a suspicious pattern), and the model adjusts severity/
  confidence accordingly.
- Shows recommendation quality for a "contained but needs follow-up"
  scenario.

---

## Test Case 5: Harmless / Insufficient-Information Input

**Input:**
```
User reported their laptop feels a bit slow today.
```

**Expected type of result:**
- `severity` of Low.
- `summary` should explicitly state that there is insufficient technical
  evidence to determine whether this is a security issue.
- `confidence` should be low (roughly 0-30).
- `indicators` should likely be an empty list, since no concrete
  technical evidence was provided.
- `recommended_actions` may suggest gathering more information (e.g.,
  checking CPU/process activity) rather than asserting a specific threat.

**What this demonstrates:**
- The system prompt's instruction to avoid inventing facts and to admit
  uncertainty is working correctly.
- The application does not produce false positives or fabricated
  technical details when given vague, non-technical input.
- Confirms the "do not invent facts" requirement from the assignment.

---

## How to Run These Tests

1. Start the Flask application (`python app.py`).
2. Open `http://127.0.0.1:5000` in a browser.
3. Paste each input above into the textarea and click **Analyze Alert**.
4. Compare the returned severity, threat type, indicators, and
   recommendations against the "expected type of result" described for
   that test case.

Alternatively, test the API directly:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"alert": "Multiple failed login attempts (12) for user jsmith from IP 203.0.113.45 within 3 minutes, followed by a successful login."}'
```
