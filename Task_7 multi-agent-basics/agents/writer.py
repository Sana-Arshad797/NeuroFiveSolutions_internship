"""
Writer Agent
------------
This is Agent 1 in the pipeline. Its only job is to produce a first draft
of content on a given topic. It knows nothing about editing — that is the
Editor Agent's job (see agents/editor.py).
"""

from openai import OpenAI

# This system prompt defines the Writer Agent's persona and responsibilities.
WRITER_SYSTEM_PROMPT = (
    "You are the Writer Agent. Your responsibility is to create a clear, "
    "accurate, well-structured first draft about the user's topic. Focus on "
    "useful information, logical structure, readability, and appropriate "
    "detail. Do not act as an editor; produce the initial draft."
)


def generate_draft(client: OpenAI, topic: str, model: str = "gpt-4o-mini") -> str:
    """
    Makes API Call #1: asks the Writer Agent to draft content on `topic`.

    Args:
        client: An initialized OpenAI client.
        topic: The topic to write about.
        model: The OpenAI model to use.

    Returns:
        The raw draft text produced by the Writer Agent.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": WRITER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Write a draft about: {topic}"},
        ],
    )

    # response.choices[0].message.content holds the model's reply text.
    return response.choices[0].message.content.strip()
