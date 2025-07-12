# config.py (Final, Clean Version)
import os
from dotenv import load_dotenv

# This line loads the variables from your .env file into the environment
load_dotenv()

# These lines securely read the loaded variables for the rest of your app to use
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")