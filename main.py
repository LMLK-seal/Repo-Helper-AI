# main.py (Final, Robust Version)
import hmac
import hashlib
from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
# Import all the keys we need to pass
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME, GITHUB_WEBHOOK_SECRET, GEMINI_API_KEY
from github_handler import handle_issue_opened

app = FastAPI()

def verify_signature(body: bytes, signature: str):
    # ... (this function is unchanged) ...
    if not signature:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(GITHUB_WEBHOOK_SECRET.encode('utf-8'), msg=body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")

@app.post("/api/github/webhook")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str = Header(None)
):
    raw_body = await request.body()
    verify_signature(raw_body, x_hub_signature_256)
    payload = await request.json()
    event = request.headers.get('x-github-event')

    if event == "issues" and payload.get("action") == "opened":
        
        # <-- CRITICAL CHANGE: Add the Gemini key to the dictionary
        config_to_pass = {
            "GITHUB_TOKEN": GITHUB_TOKEN,
            "REPO_OWNER": REPO_OWNER,
            "REPO_NAME": REPO_NAME,
            "GEMINI_API_KEY": GEMINI_API_KEY # <-- The new line
        }
        
        background_tasks.add_task(handle_issue_opened, payload, config_to_pass)
        
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Repo Helper AI is running."}