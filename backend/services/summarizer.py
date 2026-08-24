import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


def generate_summary(text: str, length: str) -> dict:
    length_instructions = {
        "short": "Keep the summary concise, around 100 words.",
        "medium": "Provide a balanced summary, around 250 words.",
        "long": "Provide a detailed summary, around 500 words.",
    }

    instruction = length_instructions.get(
        length.lower(),
        length_instructions["medium"],
    )

    prompt = f"""
You are a document summarization assistant.

Analyze the document below and return a JSON object with exactly these fields:

summary:
A clear summary of the document.

key_points:
An array containing the 4 to 6 most important points.

Summary requirement:
{instruction}

Do not invent facts that are not present in the document.

Document:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )

    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        raise RuntimeError("The AI returned an invalid response")

    return {
    "summary": result.get("summary", ""),
    "key_points": result.get("key_points", []),
}