# github_handler.py (Triage-Only, Memory-Efficient Version)
import traceback
from github import Github
import ai_services # We still use this for the initial triage

def handle_issue_opened(payload: dict, config: dict):
    """
    This function runs in the background to process a new GitHub issue.
    It classifies the issue and posts a confirmation, but does NOT answer questions.
    This version is designed to be lightweight and run on memory-constrained servers.
    """
    print("--- Background task started (Triage-Only Mode). ---")
    try:
        # Initialize the GitHub client INSIDE the function with the passed token
        g = Github(config["GITHUB_TOKEN"])
        gemini_api_key = config["GEMINI_API_KEY"]

        issue_data = payload['issue']
        issue_number = issue_data['number']
        title = issue_data['title']
        body = issue_data.get('body', '')
        user_login = issue_data['user']['login']
        print(f"Processing issue #{issue_number}: '{title}'")

        repo = g.get_repo(f"{config['REPO_OWNER']}/{config['REPO_NAME']}")
        issue = repo.get_issue(number=issue_number)
        print("Successfully connected to the issue.")

        # Triage with AI (This part remains)
        triage_prompt = ai_services.get_triage_prompt(title, body)
        category = ai_services.generate_response(gemini_api_key, triage_prompt)
        print(f"Issue classified as: {category}")

        # Labeling logic (This part remains)
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

        # --- NEW SIMPLIFIED TRIAGE-ONLY LOGIC ---
        # This block replaces the entire "if category in..." RAG logic.
        
        triage_messages = {
            "[General Question]": "Thank you for your question! A human maintainer will be with you shortly.",
            "[Installation Problem]": "Thank you for reporting this installation issue. A maintainer will help you troubleshoot soon.",
            "[Bug Report]": "Thank you for your submission! The team has been notified of this potential bug.",
            "[Feature Request]": "Thank you for the great idea! This feature request has been logged for the team to review."
        }
        category_name = category.strip('[]')
        
        # Get the specific message, or a default one if the category is unknown
        message = triage_messages.get(category, f"This issue has been automatically triaged as a **{category_name}**.")

        comment_body = f"Hello @{user_login}, {message} A maintainer will look at it soon."
        issue.create_comment(comment_body)
        print(f"SUCCESS: Posted triage-only confirmation to issue #{issue_number}.")
        # --- END OF NEW SIMPLIFIED LOGIC ---

    except Exception:
        print("\n!!!!!!!!!! AN ERROR OCCURRED IN THE BACKGROUND HANDLER !!!!!!!!!!\n")
        traceback.print_exc()
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")