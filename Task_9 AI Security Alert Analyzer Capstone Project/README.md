# AI Security Alert Analyzer

An AI-powered web application that helps analysts quickly understand and
triage cybersecurity alerts, suspicious logs, and incident descriptions by
turning free-text input into a structured, actionable risk assessment.

Built as a Generative AI & Prompt Engineering capstone project.

---

## Problem

Security teams are flooded with alerts every day — failed logins, endpoint
detections, firewall events, antivirus hits — and many of these alerts are
just raw, unstructured text. Junior analysts and small teams without a
mature SOC (Security Operations Center) often struggle to quickly:

- Judge how severe an alert really is.
- Identify what type of threat it might represent.
- Know what indicators actually matter.
- Decide on a reasonable first response.

Manually triaging every alert is slow and inconsistent, especially for
teams without dedicated security analysts on staff.

## Solution

This application lets a user paste a raw security alert or log into a
simple web interface. The alert is sent to an OpenAI model through a Flask
backend, using a carefully engineered system prompt that instructs the
model to act as a cybersecurity analyst. The model returns a **structured
JSON assessment** — severity, threat type, summary, indicators, and
recommended actions — which the frontend renders in a clean, readable
dashboard.

The system prompt explicitly instructs the model to reason only from the
evidence provided, to admit when there isn't enough information, and to
never provide offensive/attack instructions — keeping the tool safe,
defensive, and honest about uncertainty.

## Features

- Clean, responsive, cybersecurity-themed web dashboard.
- Large textarea for pasting alerts/logs, with a live character counter.
- "Load Example" button to instantly try a realistic sample alert.
- Structured AI analysis: severity, threat type, summary, indicators,
  recommended actions, and a confidence score (0-100).
- Clear loading state while the AI is processing.
- Friendly error messages for invalid input or API failures.
- Backend input validation (length limits, type checks).
- Backend validation of the AI's JSON output before it ever reaches the
  frontend.
- API key is kept server-side only — never exposed to frontend JavaScript.

## Tech Stack

- **Backend:** Python, Flask
- **AI:** OpenAI API (Chat Completions, JSON mode)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Config:** python-dotenv (`.env` file for secrets)

No React, Next.js, LangChain, or other heavy frameworks are used — the
project is intentionally kept simple and easy to read end-to-end.

## Architecture

```
User (browser)
    │
    │  1. Pastes alert text, clicks "Analyze Alert"
    ▼
Frontend (HTML/CSS/JS)
    │
    │  2. POST /api/analyze  { "alert": "..." }
    ▼
Flask Backend (app.py)
    │
    │  3. Validates input (length, type)
    │  4. Sends system prompt + alert to OpenAI API
    ▼
OpenAI API
    │
    │  5. Returns structured JSON analysis
    ▼
Flask Backend (app.py)
    │
    │  6. Parses & validates JSON schema
    │  7. Returns { "success": true, "analysis": {...} }
    ▼
Frontend (HTML/CSS/JS)
    │
    │  8. Renders severity, threat type, summary,
    │     indicators, recommended actions, confidence
    ▼
User sees a structured security assessment
```

## Prompt Engineering

The core of this project is the **system prompt** defined in
[`prompts.py`](./prompts.py). It instructs the model to:

- Act strictly as a defensive cybersecurity analyst.
- Analyze *only* the information present in the input — never invent
  hostnames, IPs, usernames, or other specific facts.
- Explicitly say when there isn't enough evidence to reach a confident
  conclusion (and lower the confidence score accordingly).
- Classify the likely threat category and assign a severity level that
  reflects the actual evidence, not a worst-case assumption.
- Extract only indicators that literally appear in the input text.
- Give practical, defensive recommendations — never offensive or
  exploit-related instructions.
- Return **only** a single JSON object matching a strict schema, with no
  extra commentary or markdown formatting.

Structured output matters here for two reasons: it makes the AI's
reasoning **machine-readable** so the frontend can render consistent,
predictable sections, and it forces the model to explicitly commit to a
severity, threat type, and confidence score rather than producing vague,
free-form prose that would be harder to act on.

The backend additionally validates that the returned JSON matches the
expected schema (`app.py`, `validate_ai_response`) before ever sending it
to the frontend, so malformed or unexpected AI output fails safely with a
clear error instead of breaking the UI.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-security-alert-analyzer.git
cd ai-security-alert-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```bash
cp .env.example .env
```

### 5. Add your OpenAI API key

Open `.env` and set your key:

```text
OPENAI_API_KEY=your_api_key_here
```

### 6. Run the Flask application

```bash
python app.py
```

### 7. Open the local URL

Visit the following in your browser:

```
http://127.0.0.1:5000
```

## Environment Variables

Create a `.env` file (never commit it) based on `.env.example`:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_MODEL` is optional and defaults to `gpt-4o-mini` if not set.

## Testing

See [`tests/test_cases.md`](./tests/test_cases.md) for five realistic
manual test cases covering:

1. Multiple failed login attempts (brute force / credential access).
2. Suspicious PowerShell activity spawned from Microsoft Word.
3. An unusual outbound network connection (possible C2 activity).
4. A confirmed malware detection alert.
5. A vague, non-technical input with insufficient evidence.

Each test case documents the input, the *expected type* of result (exact
AI wording will vary between runs), and what the test demonstrates about
the application's behavior — including its ability to admit uncertainty
rather than inventing facts.

## Limitations

This is an **educational, AI-assisted triage tool**. It is designed to
help a user quickly understand and prioritize a single alert — it is
**not** a replacement for a professional SOC investigation, a certified
incident responder, or an enterprise security platform. AI-generated
severity ratings and recommendations should always be reviewed by a
qualified analyst before any action is taken, especially in production
environments.

## Future Improvements

- Map identified threats to the **MITRE ATT&CK** framework for
  standardized threat classification.
- Add **Retrieval-Augmented Generation (RAG)** using internal
  cybersecurity documentation or threat intelligence feeds for more
  context-aware analysis.
- Integrate directly with a **SIEM** to analyze alerts in real time.
- Add **user authentication** for multi-analyst environments.
- Store a **persistent history** of analyzed alerts for auditing and
  trend analysis.
- Allow analysts to **export reports as PDF** for documentation and
  incident reporting.
