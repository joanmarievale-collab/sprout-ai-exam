import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AgentLLM:
    def reason(self, sentiment: str, confidence: float, user_message: str) -> str:
        prompt = f"""
You are a customer support agent.

User message:
"{user_message}"

Sentiment: {sentiment}
Confidence: {confidence}

Explain briefly what the agent should do next.
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return completion.choices[0].message.content.strip()
