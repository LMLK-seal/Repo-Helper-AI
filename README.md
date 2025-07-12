# Repo Helper AI 🤖

An autonomous AI-powered assistant that automatically answers questions and triages issues on a GitHub repository using Google's Gemini API and a local vector database.

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Framework](https://img.shields.io/badge/framework-FastAPI-009688.svg)
![AI Model](https://img.shields.io/badge/AI%20Model-Gemini%201.5%20Flash-F6B900.svg)
![Vector DB](https://img.shields.io/badge/Vector%20DB-ChromaDB-4169E1.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Repo Helper AI acts as a smart assistant for your GitHub repository. By listening for new issues via webhooks, it leverages the power of large language models and your project's documentation to automatically classify issues and provide relevant answers to common questions, significantly reducing the burden on human maintainers.

---

✨ Features
-----------

*   **Intelligent Issue Triage:** Automatically classifies newly opened issues into categories like Bug Report, Feature Request, Question, or Installation Problem using AI.
*   **Context-Aware Answers (RAG):** Uses a Retrieval-Augmented Generation (RAG) system powered by ChromaDB and your documentation (`/docs` folder) to find relevant information and answer user questions directly within the issue thread.
*   **Automated GitHub Actions:** Posts AI-generated answers as comments and applies relevant labels to issues using the GitHub API.
*   **Autonomous Webhook Listener:** Runs as a FastAPI application, triggered automatically by configured GitHub webhooks.
*   **Self-Hosted Knowledge Base:** Stores and queries your documentation using a local ChromaDB instance (typically run via Docker), keeping your data private.
*   **Configurable:** Easily set up and configure the bot using environment variables (`.env`).

---

⚙️ How It Works
--------------

The system operates on an event-driven architecture triggered by GitHub webhooks:

1.  **Webhook Trigger:** A user creates a new issue on GitHub. A configured webhook sends the issue details (payload) to your running application.
2.  **FastAPI Server:** A self-hosted Python server built with FastAPI receives and validates the webhook payload.
3.  **AI Triage:** The server makes a call to the configured Gemini API to classify the issue type based on its title and body.
4.  **Vector DB Query (RAG):** If the issue is classified as a "Question" or "Installation Problem", the server queries a local ChromaDB vector database (which contains indexed knowledge from the `/docs` folder) to find the most relevant documentation chunks based on the user's question.
5.  **AI Answer Generation:** The server makes a second call to the Gemini API, providing the user's full question and the retrieved context from the vector database. Gemini uses this information to generate a helpful, contextually relevant answer.
6.  **GitHub API Action:** The server uses the PyGithub library to interact with the GitHub API, posting the generated answer as a comment on the issue and applying the appropriate labels based on the AI triage result.

---

📚 Tech Stack
-------------

*   **Python:** The core programming language.
*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs, used here to receive webhooks.
*   **uvicorn:** An ASGI server that runs the FastAPI application.
*   **python-dotenv:** For loading environment variables from a `.env` file.
*   **PyGithub:** A Python library to interact with the GitHub API.
*   **Google Generative AI:** Python client for accessing the Gemini API for AI tasks (triage and answering).
*   **ChromaDB:** An open-source vector database used to store and query embeddings of your project's documentation.
*   **Docker:** Used to easily run the ChromaDB service.

---

🚀 Installation
--------------

Follow these steps to get your own Repo Helper AI running.

### 1. Prerequisites

*   Python 3.9+
*   Docker (to run the ChromaDB vector database)
*   A GitHub repository where you want to deploy the bot.
*   A GitHub Personal Access Token (classic) with `repo` scope.
*   A Google Gemini API key from Google AI Studio.
*   A strong, random string for your GitHub webhook secret.

### 2. Clone the Repository

```bash
git clone https://github.com/LMLK-seal/repo-helper-ai.git 
cd repo-helper-ai
```

### 3. Configure Your Environment

This project uses a `.env` file to manage secret keys and configuration.

*   Open the `.env` file and fill in your details:
    ```dotenv
    GITHUB_TOKEN=YOUR_GITHUB_PAT
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    GITHUB_WEBHOOK_SECRET=YOUR_RANDOM_SECRET_STRING
    REPO_OWNER=your-github-username
    REPO_NAME=your-repository-name
    ```
    *   Replace placeholders with your actual values.

### 4. Create a Virtual Environment & Install Dependencies

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate
# Or on macOS/Linux:
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

---

🛠️ Usage (Local Development)
-----------------------------

These instructions are for running the bot on your local machine for development and testing purposes.

### 1. Start the Vector Database

In a separate terminal, start the ChromaDB service using Docker. This provides the knowledge base for your documentation.

```bash
docker run -p 8000:8000 chromadb/chroma
```

### 2. Index Your Documentation

Before the bot can answer questions based on your documentation, you need to index it. This script reads files from the `./docs` directory and stores their embeddings in ChromaDB.

```bash
python vector_db.py
```
*(You should re-run this command whenever you add, remove, or significantly change files in your `./docs` folder.)*

### 3. Run the Bot Server

Start the main FastAPI application server. The `--reload` flag is useful for development, but you would typically use a process manager like `gunicorn` or `pm2` for production deployment (see Deployment Guide in `docs/06_deployment.md`).

```bash
uvicorn main:app --reload
```

### 4. Configure the GitHub Webhook

The bot is now running, but GitHub needs to know where to send issue events.

1.  Since the bot is likely running locally, you'll need a way for GitHub to reach it over the internet. Tools like `ngrok` or `localtunnel` can help. For example, using ngrok:
    ```bash
    ngrok http 8000
    ```
    Copy the `https://` forwarding URL provided by ngrok (e.g., `https://abcdef123456.ngrok.io`).
2.  In your GitHub repository, go to **Settings > Webhooks > Add webhook**.
3.  **Payload URL:** Paste your public forwarding URL and add `/api/github/webhook` to the end (e.g., `https://abcdef123456.ngrok.io/api/github/webhook`).
4.  **Content type:** Set to `application/json`.
5.  **Secret:** Paste the `GITHUB_WEBHOOK_SECRET` from your `.env` file. **This is crucial for security.**
6.  **Which events...?:** Select "Let me select individual events." and check **Issues**.
7.  Ensure "Active" is checked.
8.  Click **Add webhook**.

Your Repo Helper AI is now live and ready to assist with new issues opened in your repository!


---

☁️ Deployment (Production)
-----------------------

To run the bot 24/7 without needing to keep your local computer on, you should deploy it to a cloud service. Below is a guide for deploying on **Render**, which offers a free tier suitable for this project.

### Prerequisites for Deployment

1.  **Push Your Code to GitHub:** Your project, including all `.py` files, the `docs` folder, `requirements.txt`, and your professional `README.md`, must be in a GitHub repository.
2.  **Create a `build.sh` file:** Some cloud services need help setting up. Create a file named `build.sh` in your project's root directory with the following content. This script will run your `vector_db.py` script automatically during deployment to build the knowledge base.

    ```bash
    #!/usr/bin/env bash
    # exit on error
    set -o errexit

    pip install -r requirements.txt

    # Run the vector DB indexing script
    python vector_db.py
    ```

### Deploying to Render

1.  **Sign up** for a free account at [render.com](https://render.com/) using your GitHub account.
2.  In the Render Dashboard, click **New +** and select **Web Service**.
3.  Connect the GitHub repository containing your bot's code.
4.  Give your service a unique name. The region does not matter.
5.  Set the **Build Command** to: `./build.sh`
6.  Set the **Start Command** to: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
7.  Under the **Advanced** section, go to **Environment Variables**. Add all the keys from your local `.env` file here (`GITHUB_TOKEN`, `GEMINI_API_KEY`, etc.). **Do not use a `.env` file in production.**
8.  Click **Create Web Service**. Render will automatically build and deploy your application.
9.  Once deployed, Render will give you a public `https://...onrender.com` URL. Use **this URL** for your GitHub webhook's Payload URL. Now your bot is live 24/7!

---

▶️ How to Trigger the Bot
-----------------------

Once installed and configured, the bot is automatically triggered when a new issue is opened in the configured GitHub repository.

*   **Open an issue:** Simply create a new issue in your repository.
*   **Observe:** The bot will automatically classify the issue and, if it's a question or installation problem, attempt to provide an answer based on your documentation within a few moments by posting a comment. It will also add relevant labels.

---

🤝 Contributing
--------------

Contributions are welcome! If you'd like to contribute, please refer to the `docs/contributing.md` file for detailed guidelines on reporting bugs, suggesting enhancements, and submitting pull requests.

---

📄 License
---------

This project is licensed under the MIT License. See the `docs/license.md` file for details.

---
