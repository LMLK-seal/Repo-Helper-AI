# Customizing the AI's Behavior

You can change the personality and instructions of the AI by editing the prompts in the `ai_services.py` file.

## Changing the Answering Persona
To change how the bot answers questions, modify the `get_answer_prompt` function. You can make it more formal, more friendly, or even ask it to respond in a specific format like JSON.

**Example: A more concise persona:**
> "You are a factual, to-the-point AI assistant. Answer the user's question directly using the provided context. Do not add conversational filler."

## Changing the Triage Logic
To add new categories for issue triage, modify the `get_triage_prompt` function.
1.  Add your new category to the list, e.g., `[Documentation Error]`.
2.  Update the `label_map` dictionary in `github_handler.py` to associate your new category with a GitHub label.