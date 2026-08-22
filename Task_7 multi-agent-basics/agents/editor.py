"""
Editor/Critic Agent
--------------------
This is Agent 2 in the pipeline. It receives Agent 1's raw draft as input
(this is the key "multi-agent" step — one agent's output feeds the next
agent's input) and produces an improved final draft plus a list of the
improvements it made.
"""

from openai import OpenAI

# This system prompt defines the Editor Agent's persona and responsibilities.
EDITOR_SYSTEM_PROMPT = (
    "You are the Editor/Critic Agent. Your responsibility is to critically "
    "review the Writer Agent's draft and produce an improved final version. "
    "Check clarity, organization, grammar, repetition, factual consistency, "
    "weak explanations, and missing important points. Preserve the original "
    "intent while improving the quality. After the improved draft, provide a "
    "concise list of the major improvements you made."
)


def edit_draft(client: OpenAI, topic: str, raw_draft: str, model: str = "gpt-4o-mini") -> str:
    """
    Makes API Call #2: sends Agent 1's raw draft to the Editor Agent for
    review and improvement.

    Args:
        client: An initialized OpenAI client.
        topic: The original topic (given as context to the Editor).
        raw_draft: The Writer Agent's draft text, produced by generate_draft().
                   This is the value that makes this a genuine two-agent
                   pipeline: Agent 2 literally receives Agent 1's output.
        model: The OpenAI model to use.

    Returns:
        The Editor Agent's full response: the improved draft followed by
        an "IMPROVEMENTS" section listing what was changed.
    """
    user_message = (
        f"Topic: {topic}\n\n"
        f"Here is the Writer Agent's raw draft:\n\n"
        f"{raw_draft}\n\n"
        f"Please review it and produce:\n"
        f"1. An improved final draft.\n"
        f"2. A clearly labeled section titled 'IMPROVEMENTS' listing the "
        f"major changes you made as bullet points."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": EDITOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content.strip()
