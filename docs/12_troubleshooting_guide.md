# Comprehensive Troubleshooting Guide

This guide provides solutions to common problems encountered during the setup and operation of the Repo Helper AI. If your issue is not listed here, please consult the `bot.log` file for detailed error messages.

---

### 1. Installation & Setup Issues

These errors typically occur before the application server is running.

#### Problem `ModuleNotFoundError No module named 'some_package'`

 You see an error like `ModuleNotFoundError` when running a Python script.

Solution This means the required Python packages are not installed in the Python environment you are currently using.

1.  Activate Virtual Environment Ensure your virtual environment is active. On Windows, run `.venvScriptsactivate`. On macOSLinux, run `source venvbinactivate`. You should see `(venv)` at the start of your terminal prompt.
2.  Install Requirements Run the installation command again
    ```bash
    pip install -r requirements.txt
    ```

#### Problem C++ Compiler Error

 During `pip install`, you see an error like `Microsoft Visual C++ 14.0 or greater is required`.

Solution One of the dependencies (often for `chromadb`) needs to be compiled from source code, which requires a C++ compiler.

1.  Download the Visual Studio Build Tools from the official Microsoft website.
2.  Run the installer and select the Desktop development with C++ workload.
3.  After installation, restart your terminal and try running `pip install -r requirements.txt` again.

#### Problem `'docker' is not recognized` or `Cannot connect to the Docker daemon`

 You see this error when trying to run the `docker run ...` command.

Solution The Docker service is not running or is not available in your terminal's path.

1.  Start Docker Desktop Find the Docker Desktop application on your computer and launch it.
2.  Wait for it to initialize. The Docker icon in your system tray should be steady (not animating).
3.  Once it's running, try the `docker run ...` command again.

#### Problem `'ngrok' is not recognized`

 You see this error when trying to run `ngrok http 8000`.

Solution The `ngrok.exe` program is not in your system's PATH.

1.  Download ngrok from the official ngrok website.
2.  Unzip the file to get `ngrok.exe`.
3.  For simplicity, place the `ngrok.exe` file in your project's root directory.
4.  Run the command from your project directory using `.ngrok.exe http 8000`.

---

### 2. Runtime & Webhook Issues

These errors occur after the `uvicorn` server is running and you are testing the GitHub webhook connection.

#### Problem Webhook delivery fails with a `403 Forbidden` error.

 In the GitHub Webhook settings, the Recent Deliveries tab shows a red `X` and a `403` response code.

Solution This is a security success! It means your server received the request but rejected it because the `GITHUB_WEBHOOK_SECRET` does not match.

1.  Open your `.env` file and carefully copy the value for `GITHUB_WEBHOOK_SECRET`.
2.  Go to your GitHub repository's Settings  Webhooks. Click Edit on your webhook.
3.  Delete the old value in the `Secret` box and paste the correct one.
4.  Save the webhook.
5.  Restart your `uvicorn` server to ensure it loads any potential changes.
6.  Use the Redeliver button in the webhook settings to test again.

#### Problem The bot fails with a `404 Not Found` error.

 Your `bot.log` or terminal shows a `github.GithubException.UnknownObjectException 404 {message Not Found, ...}` traceback.

Solution This error means the bot could not find your repository. This is almost always due to an incorrect configuration in your `.env` file.

1.  Check `REPO_OWNER` and `REPO_NAME` Ensure these values in your `.env` file exactly match your GitHub repository URL (`httpsgithub.comREPO_OWNERREPO_NAME`). The owner and name are case-sensitive.
2.  Check `GITHUB_TOKEN` Ensure your token is correct and has not expired. Most importantly, confirm that when you created the token, you selected the `repo` scope.

#### Problem The bot fails with a Gemini API error.

 The bot posts a comment saying An error occurred while contacting the AI model, or your log shows an error from `google-generativeai`.

Solution There is a problem with your Gemini API key or configuration.

1.  Check `GEMINI_API_KEY` Ensure the key in your `.env` file is correct and has no extra spaces or missing characters.
2.  Check the Model Name In `ai_services.py`, ensure the model name (e.g., `'gemini-1.5-flash-latest'`) matches a model that your API key is authorized to use.
3.  Check API Enabled Go to your Google Cloud project dashboard and ensure the Generative Language API is enabled.

#### Problem Webhook delivery succeeds (`200 OK`), but the bot does nothing.

 The `uvicorn` terminal shows a `200 OK` but no further logs appear in the terminal or `bot.log`. The bot never posts a comment.

Solution This is a subtle but critical issue related to how background tasks work. The main application is not successfully passing the configuration secrets to the background worker.

The current project code is structured to solve this by explicitly passing a `config` dictionary. If you encounter this, ensure your `main.py` and `github_handler.py` match the final, robust versions from the project guide, which are designed to prevent this amnesiac worker problem.

---

### 3. AI Behavior & Content Issues

#### Problem The bot gives wrong or outdated answers.

Solution The bot's brain is its documentation. Its knowledge is only as good as the files in your `docs` folder.

1.  Update Your Documentation Find the incorrect information in the relevant `.md` file inside the `docs` folder and correct it. If the information is missing, add a new `.md` file.
2.  Re-Index the Database After changing the documentation, you must teach the bot about the changes. Stop your server and run
    ```bash
    python vector_db.py
    ```
3.  Restart your server. The bot will now use the updated knowledge.

#### Problem How do I change the bot's personality

Solution The bot's personality is defined by the system prompts given to the Gemini model.

1.  Open the `ai_services.py` file.
2.  Modify the text inside the `get_answer_prompt` function to change how it answers questions.
3.  Modify the text inside the `get_triage_prompt` function to change how it classifies issues.