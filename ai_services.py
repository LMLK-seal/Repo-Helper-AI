# ai_services.py (Final, Robust Version)
import google.generativeai as genai

# NOTE: We no longer configure the client at the top level.

def get_model(api_key: str):
    """A helper function to configure and return a model instance."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash-latest')

def get_triage_prompt(title: str, body: str) -> str:
    """Creates a prompt to classify a GitHub issue. (No change here)"""
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
    """Creates a prompt to answer a question based on provided context. (No change here)"""
    return f"""
    You are a professional and knowledgeable AI assistant for the "Awesome-Project" repository.
    # ... (rest of the prompt is the same) ...
    ---
    Knowledge Base Context:
    {context}
    ---
    User's Question:
    {question}
    ---
    Your Answer:
    """

# <-- CRITICAL CHANGE: The function now requires the api_key to be passed in.
def generate_response(api_key: str, prompt: str) -> str:
    """Generates a response from the Gemini model using a provided API key."""
    try:
        model = get_model(api_key) # Get a configured model instance
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response from Gemini: {e}")
        return "An error occurred while contacting the AI model."