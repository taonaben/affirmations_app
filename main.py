from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


@app.get("/")
async def get_affirmation():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are PB — authentic, sharp, never corny. "
                    "Your affirmations for your girlfriend are deep, original, and well-worded, "
                    "with richer vocabulary and poetic charm. "
                    "Avoid clichés, keep it personal, captivating, and real."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Generate one short message for my girlfriend — it can be an affirmation, compliment, reassurance, gratitude, flirty line, or poetic note. "
                    "Make it deep, original, vocabulary-rich, slightly poetic but natural. "
                    "Avoid corny or generic phrasing; it should feel authentic, charming, and real."
                ),
            },
        ],
        max_tokens=50,
        temperature=0.7,
    )
    affirmation = response.choices[0].message.content.strip()
    return {"affirmation": affirmation}
