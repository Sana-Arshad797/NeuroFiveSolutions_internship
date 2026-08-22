"""
Multi-Agent Content Pipeline
=============================
A simple two-agent system built with plain sequential OpenAI API calls
(no LangChain, no extra frameworks):

    Agent 1 (Writer)  -> produces a raw draft on a topic
    Agent 2 (Editor)  -> reviews Agent 1's draft and improves it

This file wires the two agents together, runs the two required demo
topics automatically, lets the user try a topic of their own, and saves
each result to the outputs/ folder.
"""

import os
import re
import sys

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from agents.writer import generate_draft
from agents.editor import edit_draft

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")

# The two topics required by the assignment. The pipeline runs on both
# automatically so the multi-agent behavior is easy to demonstrate.
DEMO_TOPICS = [
    "The Importance of Cybersecurity in Artificial Intelligence",
    "Why Strong Passwords Are Important for Online Security",
]


def get_client() -> OpenAI:
    """
    Loads OPENAI_API_KEY from a local .env file and returns an OpenAI
    client. Exits with a clear, friendly message if the key is missing,
    instead of crashing with a raw stack trace.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY was not found.")
        print()
        print("To fix this:")
        print("  1. Copy .env.example to a new file named .env")
        print("  2. Open .env and paste in your real OpenAI API key")
        print("  3. Run this program again")
        sys.exit(1)

    return OpenAI(api_key=api_key)


def parse_editor_output(editor_output: str):
    """
    Splits the Editor Agent's single text response into two pieces:
    (final_draft, improvements_list).

    The Editor is instructed (in agents/editor.py) to end its response
    with a section titled "IMPROVEMENTS". This function finds that
    heading and splits the text there. If the heading is somehow
    missing, it falls back gracefully instead of crashing.
    """
    match = re.search(r"improvements", editor_output, re.IGNORECASE)

    if match:
        final_draft = editor_output[: match.start()].strip()
        improvements = editor_output[match.start():].strip()
        # Strip the heading word itself (and any ":"/"-" after it)
        improvements = re.sub(
            r"^improvements\s*[:\-]*\s*", "", improvements, flags=re.IGNORECASE
        )
    else:
        final_draft = editor_output.strip()
        improvements = "(Editor did not return a separate improvements section.)"

    return final_draft, improvements


def print_section(title: str, content: str):
    print("-" * 16 + f" {title} " + "-" * 16)
    print(content)
    print()


def run_pipeline(client: OpenAI, topic: str) -> dict:
    """
    Runs the full two-agent pipeline for a single topic.

    API Call #1 -> Writer Agent produces raw_draft.
    API Call #2 -> Editor Agent receives raw_draft (this is the actual
                   hand-off between the two agents) and returns an
                   improved draft + improvement notes.
    """
    try:
        raw_draft = generate_draft(client, topic)
        editor_output = edit_draft(client, topic, raw_draft)
    except OpenAIError as e:
        print(f"API ERROR while processing topic '{topic}': {e}")
        sys.exit(1)

    final_draft, improvements = parse_editor_output(editor_output)

    return {
        "topic": topic,
        "raw_draft": raw_draft,
        "final_draft": final_draft,
        "improvements": improvements,
    }


def display_result(result: dict, label):
    print("=" * 50)
    print(f"TOPIC {label}: {result['topic']}")
    print()
    print_section("AGENT 1: WRITER", result["raw_draft"])
    print_section("AGENT 2: EDITOR", result["final_draft"])
    print_section("EDITOR IMPROVEMENTS", result["improvements"])
    print("=" * 50)
    print()


def save_result(result: dict, filename: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Topic: {result['topic']}\n\n")
        f.write("## Agent 1 - Writer (Raw Draft)\n\n")
        f.write(result["raw_draft"] + "\n\n")
        f.write("## Agent 2 - Editor (Final Draft)\n\n")
        f.write(result["final_draft"] + "\n\n")
        f.write("## Editor Improvements\n\n")
        f.write(result["improvements"] + "\n")

    print(f"Saved: {path}")


def main():
    print("=" * 50)
    print("MULTI-AGENT CONTENT PIPELINE")
    print("=" * 50)
    print()

    client = get_client()

    # Step 1: run the two required demo topics automatically.
    for i, topic in enumerate(DEMO_TOPICS, start=1):
        result = run_pipeline(client, topic)
        display_result(result, i)
        save_result(result, f"topic{i}_result.md")

    # Step 2: let the user try their own topic if they want to.
    custom_topic = input(
        "Enter your own topic to run the pipeline (or press Enter to skip): "
    ).strip()

    if custom_topic:
        result = run_pipeline(client, custom_topic)
        display_result(result, "Custom")


if __name__ == "__main__":
    main()
