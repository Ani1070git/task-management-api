from groq import Groq
import os

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_task_from_message(message: str):
    client = get_client()
    prompt = f"""Extract only the core task from this message.
Do not return the full sentence. Return only what needs to be done.

Example:
Input: "Add a task to buy groceries tomorrow"
Output: "Buy groceries tomorrow"

Now extract from this:
Input: {message}
Output:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()