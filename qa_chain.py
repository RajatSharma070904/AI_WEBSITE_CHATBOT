import requests

SYSTEM_PROMPT = """
You are a website-based AI assistant.

STRICT RULES (DO NOT BREAK):
- Answer ONLY using the provided website content.
- DO NOT add any introductory or concluding sentences on your own.
- DO NOT say phrases like "The answer is available on the provided website".
- If the answer is NOT present in the content, respond with EXACTLY this sentence and nothing else:
"The answer is not available on the provided website."
"""

def create_qa_chain(vector_store):
    def ask(question, chat_history):
        
        docs = vector_store.similarity_search(question, k=4)

        if not docs:
            return "The answer is not available on the provided website."

        context = "\n\n".join(d.page_content for d in docs)

        prompt = f"""
{SYSTEM_PROMPT}

Website Content:
{context}

Question:
{question}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        answer = response.json().get("response", "").strip()

        
        if answer.lower().startswith("the answer is available"):
            answer = answer.replace(
                "The answer is available on the provided website.", ""
            ).strip()

        if not answer:
            return "The answer is not available on the provided website."

        return answer

    return ask
