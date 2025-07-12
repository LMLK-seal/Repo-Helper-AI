# github_handler.py (Final, Clean Version)
import traceback
from github import Github
import ai_services
import vector_db

def handle_issue_opened(payload: dict, config: dict):
    """
    This function runs in the background to process a new GitHub issue.
    It receives its configuration directly from the main app.
    """
    print("--- Background task started. ---")
    try:
        # Initialize the GitHub client INSIDE the function with the passed token
        g = Github(config["GITHUB_TOKEN"])

        issue_data = payload['issue']
        issue_number = issue_data['number']
        title = issue_data['title']
        body = issue_data.get('body', '')
        user_login = issue_data['user']['login']
        print(f"Processing issue #{issue_number}: '{title}'")

        repo = g.get_repo(f"{config['REPO_OWNER']}/{config['REPO_NAME']}")
        issue = repo.get_issue(number=issue_number)
        print("Successfully connected to the issue.")

        # Triage with AI
        triage_prompt = ai_services.get_triage_prompt(title, body)
        category = ai_services.generate_response(triage_prompt)
        print(f"Issue classified as: {category}")

        # Labeling logic
        label_map = {
            "[General Question]": "question",
            "[Bug Report]": "bug",
            "[Feature Request]": "enhancement",
            "[Installation Problem]": "installation-help",
        }
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
            
            answer_prompt = ai_services.get_answer_prompt(full_question, context)
            ai_answer = ai_services.generate_response(answer_prompt)
            print("AI answer generated.")
            
            comment_body = f"Hello @{user_login}!\n\n{ai_answer}\n\n---\n*I am an AI assistant. If this answer is incorrect or does not resolve your issue, a human maintainer will review it shortly.*"
            issue.create_comment(comment_body)
            print(f"SUCCESS: Posted AI answer to issue #{issue_number}.")
        else:
            # --- THIS IS THE NEW, IMPROVED BLOCK ---
            # Create more specific confirmation messages
            triage_messages = {
                "[Bug Report]": "Thank you for your submission! The team has been notified of this potential bug.",
                "[Feature Request]": "Thank you for the great idea! This feature request has been logged for the team to review."
            }
            # Get the specific message, or a default one
            category_name = category.strip('[]')
            message = triage_messages.get(category, f"This issue has been automatically triaged as a **{category_name}**.")

            comment_body = f"Hello @{user_login}, {message} A maintainer will look at it soon."
            issue.create_comment(comment_body)
            print(f"SUCCESS: Posted triage confirmation to issue #{issue_number}.")
            # --- END OF NEW BLOCK ---

    except Exception:
        print("\n!!!!!!!!!! AN ERROR OCCURRED IN THE BACKGROUND HANDLER !!!!!!!!!!\n")
        traceback.print_exc()
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")