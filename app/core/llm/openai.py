from openai import AsyncOpenAI
from app.core.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a retrieval-based assistant.

Rules:
- Answer ONLY using the provided Context.
- If the answer is NOT present in the Context, say exactly:
  "I don't have enough information to answer that."
- Do NOT guess.
"""

async def stream_llm(prompt: str):
    # sync generator that yields tokens from OpenAI in real time.

    # What happens here:
        # Connection opens to OpenAI
        # Model starts generating tokens
        # Tokens arrive incrementally
    stream = await client.chat.completions.create(
        model='gpt-4o-mini', 

        # This part is about how you talk to the LLM, not your app users.
        messages=[
            # This is: A hidden instruction, Defines model behavior, User does NOT see it.
            # Examples: You are a strict teacher. You answer in bullet points.. You never hallucinate.
            # Think of it as: How should the brain behave?
            # {"role": "system", "content": "You are a helpful assistant."},

            {"role": "system", "content": SYSTEM_PROMPT},
            # This is: The actual question, Combined with context, Treated as if user typed it.
            # But again: This is not shown to the real end-user unless YOU show it.
            {"role": "user", "content": prompt},
        ],
        stream=True)
    
    # OpenAI streaming response
    # Consume streamed tokens
    # Each chunk is a partial response
        # Not a full sentence. Could be "Hel", "lo", " world"
    # chunk = word
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
    # delta = “what changed since last chunk”
