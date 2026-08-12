# Noor & Husn Café – NoorBot Chatbot 🌸☕

An AI-powered chatbot that uses the **Google Gemini API** and acts as a
table-booking assistant for "Noor & Husn Café".

**Name meaning:** Noor (light/radiance) + Husn (beauty) = "Graceful Glow" —
that's why the bot's tone is kept warm and welcoming.

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `noor_husn_chatbot.py` | Main script — the chatbot runs here |
| `.env.example` | Shows the format for storing your API key |
| `.gitignore` | Keeps `.env` out of GitHub when you push |
| `README.md` | This file — full explanation |

---

## 🔑 Where to Add Your API Key (Step by Step)

1. Copy `.env.example` and rename the copy to: **`.env`**
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux use `cp .env.example .env`)

2. Open the `.env` file in any text editor (Notepad, VS Code, etc.)

3. You'll see this line:
   ```
   GEMINI_API_KEY=paste_your_gemini_api_key_here
   ```

4. Replace the placeholder with your actual Gemini API key, for example:
   ```
   GEMINI_API_KEY=AIzaSyD4xxxxxxxxxxxxxxxxxxxxxxx
   ```

5. Save the file. **That's it — the script will automatically pick up
   this key.** You never need to type the key directly into the code.

⚠️ **Important:** Never push the `.env` file to GitHub. The `.gitignore`
file already handles this automatically, so you don't need to worry.

---

## ⚙️ Setup & Run (Step by Step)

1. **Make sure Python is installed** (3.8+). Check with:
   ```bash
   python --version
   ```

2. **Install the required libraries:**
   ```bash
   pip install google-genai python-dotenv
   ```

3. **Add your API key** (see the steps above)

4. **Run the script:**
   ```bash
   python noor_husn_chatbot.py
   ```

5. The terminal will automatically send 5 test messages and print
   NoorBot's replies. After that, you can type your own messages and
   chat with NoorBot directly — type `exit` or `quit` to stop.

---

## 🧠 How the Project Works (Full Explanation)

### 1. Loading the API Key
```python
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
```
This code safely loads the key from the `.env` file and creates a
Gemini client using Google's official SDK (`google-genai`). The key is
never hardcoded directly in the code — this is a security best practice
(so the key isn't exposed if the code is ever shared).

### 2. System Prompt (the Bot's Persona)
```python
SYSTEM_PROMPT = """You are "NoorBot"..."""
```
This is the part that gives the bot its **character** — its name, the
café's name, what it should do (bookings, menu, hours), and how it
should react to off-topic questions. This is sent to Gemini as a
**system instruction**, so every response matches this persona.

### 3. The API Call (`ask_noorbot` function)
```python
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=user_message,
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
)
```
This function sends the user's message to Gemini along with the system
prompt, using Google's official SDK (more reliable than raw HTTP calls
and handles authentication automatically). It's wrapped in a
`try/except` block so that if the free-tier rate limit is hit, the
script shows a friendly message instead of crashing.

### 4. Testing (5 messages)
At the start of the script, there are 5 test messages — 4 are normal
booking-related questions, and 1 is **deliberately off-topic**
("write me an essay"). This checks whether the bot stays in character —
if it works correctly, it will politely decline and say it can only
help with café-related things.

### 5. Interactive Mode
After the 5 test messages run, the script enters a loop where you can
type your own messages and chat with NoorBot live in the terminal.
Type `exit` or `quit` at any time to end the conversation.

---

## 🎥 What to Do for Submission

1. Push the script to GitHub (don't push `.env` — it's already ignored)
2. Record a 2-3 minute video running the script, showing the 5 test
   responses, then typing 1-2 of your own questions in interactive mode
3. Submit the GitHub link and video

## ⚠️ Note on Free-Tier Rate Limits
Google's free tier has daily and per-minute request limits. If you see
a "Rate limit reached" message, it means the quota was hit temporarily —
this is expected behavior on the free tier, not a bug. Wait a bit (or
until the next day) and try again.
