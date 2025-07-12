# github_handler.py (Final, Robust Version)
import traceback
from github import Github
import ai_services # Our updated AI services
import vector_db

def handle_issue_opened(payload: dict, config: dict):
    """
    This function runs in the background to process a new GitHub issue.
    It receives its configuration directly from the main app.
    """
    print("--- Background task started. ---")
    try:
        g = Github(config["GITHUB_TOKEN"])
        # <-- CRITICAL CHANGE: Get the Gemini key from the passed config
        gemini_api_key = config["GEMINI_API_KEY"]

        issue_data = payload['issue']
        # ... (rest of the variable assignments are the same) ...
        issue_number = issue_data['number']
        title = issue_data['title']
        body = issue_data.get('body', '')
        user_login = issue_data['user']['login']
        print(f"Processing issue #{issue_number}: '{title}'")

        repo = g.get_repo(f"{config['REPO_OWNER']}/{config['REPO_NAME']}")
        issue = repo.get_issue(number=issue_number)
        print("Successfully connected to the issue.")

        # Triage with AI, passing the key
        triage_prompt = ai_services.get_triage_prompt(title, body)
        category = ai_services.generate_response(gemini_api_key, triage_prompt)
        print(f"Issue classified as: {category}")

        # ... (Labeling logic is the same) ...
        label_map = { "[General Question]": "question", "[Bug Report]": "bug", "[Feature Request]": "enhancement", "[Installation Problem]": "installation-help" }
        label = label_map.get(category)
        if label:
            issue.add_to_labels(label, "ai-triaged")
        else:
            issue.add_to_labels("needs-human-review")
        print("Labels added.")

        # RAG and Response logic
        if category in ["[General Question]", "[Installation Problem]"]:
            full_question = f"Title: {title}\nBody: {body}"
            context = vector_db.query_vector_db(full_question)
            print("Context retrieved from vector DB.")
            
            # Generate the answer, passing the key
            answer_prompt = ai_services.get_answer_prompt(full_question, context)
            ai_answer = ai_services.generate_response(gemini_api_key, answer_prompt)
            print("AI answer generated.")
            
            comment_body = f"Hello @{user_login}!\n\n{ai_answer}\n\n---\n*I am an AI assistant...*"
            issue.create_comment(comment_body)
            print(f"SUCCESS: Posted AI answer to issue #{issue_number}.")
        else:
            # ... (Triage confirmation logic is the same) ...
            triage_messages = { "[Bug Report]": "Thank you for your submission! The team has been notified of this potential bug.", "[Feature Request]": "Thank you for the great idea! This feature request has been logged for the team to review." }
            category_name = category.strip('[]')
            message = triage_messages.get(category, f"This issue has been automatically triaged as a **{category_name}**.")
            comment_body = f"Hello @{user_login}, {message} A maintainer will look at it soon."
            issue.create_comment(comment_body)
            print(f"SUCCESS: Posted triage confirmation to issue #{issue_number}.")

    except Exception:
        print("\n!!!!!!!!!! AN ERROR OCCURRED IN THE BACKGROUND HANDLER !!!!!!!!!!\n")
        traceback.print_exc()
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")