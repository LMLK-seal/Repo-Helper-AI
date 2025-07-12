# ai_services.py
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)
# Using the model we confirmed works with your key
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_triage_prompt(title: str, body: str) -> str:
    """Creates a prompt to classify a GitHub issue."""
    return f"""
    Analyze the following GitHub issue and classify it into one of these categories:
    [General Question], [Bug Report], [Feature Request], [Installation Problem], [Other].
    Provide ONLY the category name in brackets.

    Issue Title: {title}
    Issue Body:
    ---
    {body}
    ---
    Category:
    """

def get_answer_prompt(question: str, context: str) -> str:
    """Creates a prompt to answer a question based on provided context."""
    return f"""
    You are a professional and knowledgeable AI assistant for the "Awesome-Project" repository.
    Your primary goal is to answer user questions with precision and clarity, based ONLY on the provided "Knowledge Base Context".

    **Formatting Rules:**
    - Use clear and concise language.
    - Use markdown for formatting, including bullet points, bold text, and code blocks for commands or parameters.
    - Structure your answer logically. Start with a direct answer, then provide details.

    **Content Rules:**
    - If the context contains the answer, provide it. If possible, mention the source document (e.g., "According to the Deployment Guide...").
    - If the context does not contain a definitive answer, you MUST state: "I could not find a specific answer in the project's documentation regarding your question. A human maintainer will provide further assistance." Do not guess or infer information.

    ---
    Knowledge Base Context:
    {context}
    ---
    User's Question:
    {question}
    ---
    Your Answer:
    """

def generate_response(prompt: str) -> str:
    """Generates a response from the Gemini model."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response from Gemini: {e}")
        return "An error occurred while contacting the AI model."