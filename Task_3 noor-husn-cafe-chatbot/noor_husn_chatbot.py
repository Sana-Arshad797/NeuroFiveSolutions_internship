"""
NoorBot - Noor & Husn Café Booking Assistant
----------------------------------------------
This script calls the Google Gemini API (via the official Google SDK)
and gives the bot a "cafe booking assistant" persona through a system prompt.

Setup:
1. pip install google-genai python-dotenv
2. Create a .env file (in this same folder) containing:
   GEMINI_API_KEY=your_api_key_here
3. python noor_husn_chatbot.py
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found! Please check your .env file.")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.5-flash-lite"

# ---------------------------------------------------
# SYSTEM PROMPT: This defines the bot's persona and rules
# ---------------------------------------------------
SYSTEM_PROMPT = """
You are "NoorBot", a friendly table-booking assistant for "Noor & Husn Café".
The café's name combines "Noor" (radiance/light) and "Husn" (beauty) —
meaning "Graceful Glow" — so your tone should be warm, welcoming, and a bit poetic.

Your responsibilities:
- Take table bookings from customers (name, date, time, number of guests)
- Share café hours: Open daily from 9 AM to 11 PM
- Share café location: Main Boulevard, Gulberg, Lahore
- Give basic menu info: Coffee, tea, sandwiches, and desserts are available
- Always use a polite, warm, and professional tone

Rules:
1. Only answer questions related to the café (booking, menu, hours, location).
2. If someone asks something off-topic (weather, homework help, coding, general
   knowledge, etc.), politely decline and say: "I can only help with Noor & Husn
   café bookings and information!" then steer the conversation back.
3. When taking a booking, always ask for the name, date, time, and number of
   guests if the customer hasn't provided them.
4. Keep responses short and to the point (2-4 lines).
"""

def ask_noorbot(user_message: str) -> str:
    """Sends the user's message to NoorBot and returns its reply."""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
        )
        reply = response.text
    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            reply = "(Rate limit reached — please wait about 30-60 seconds and try again.)"
        else:
            reply = f"(Sorry, something went wrong: {error_text[:150]})"

    return reply.strip()


if __name__ == "__main__":
    # 5 test messages (including one tricky/off-topic message)
    test_messages = [
        "Hi! I'd like a table for 4 people tomorrow evening at 7 PM.",
        "What's on your menu?",
        "What time does the café open?",
        "Can you write me an essay on 'Global Warming'?",  # tricky/off-topic
        "My name is Ali, please confirm my booking.",
    ]

    print("=" * 50)
    print("NoorBot - Noor & Husn Café Assistant")
    print("=" * 50)

    for i, msg in enumerate(test_messages, start=1):
        print(f"\n[Test {i}] User: {msg}")
        bot_reply = ask_noorbot(msg)
        print(f"NoorBot: {bot_reply}")

    # ---------------------------------------------------
    # INTERACTIVE MODE: Now you can type your own questions
    # ---------------------------------------------------
    print("\n" + "=" * 50)
    print("Now you can chat with NoorBot yourself!")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("NoorBot: Thank you for visiting Noor & Husn Café. See you soon!")
            break
        if not user_input:
            continue
        reply = ask_noorbot(user_input)
        print(f"NoorBot: {reply}")
