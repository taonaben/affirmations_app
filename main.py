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
                "content": "You are a loving, supportive partner.",
            },
            {
                "role": "user",
                "content": "Give me one short, sweet daily affirmation for my girlfriend.",
            },
        ],
        max_tokens=50,
        temperature=0.7,
    )
    affirmation = response.choices[0].message.content.strip()
    return {"affirmation": affirmation}
