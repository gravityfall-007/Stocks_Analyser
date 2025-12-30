import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

def generate_llm_summary(prompt: str) -> str:
    """
    Generate an interpretive market philosophy summary.
    Non-predictive, explanatory only.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional market analyst. "
                    "You explain market structure, risk, psychology, and positioning. "
                    "You NEVER give trading advice or price predictions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=400
    )

    return response.choices[0].message.content
