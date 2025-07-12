# Deployment Guide

To run this bot 24/7, you need to deploy it to a server. Here are the recommended options.

## Option 1: Virtual Private Server (VPS)
A VPS from providers like DigitalOcean, Linode, or Vultr gives you full control.

### Setup Steps:
1.  Provision a new Ubuntu 22.04 server.
2.  Install Python 3.9+, pip, and venv.
3.  Install a process manager like `pm2` for Node.js or `gunicorn` for Python to keep the application running. For this project, you will use gunicorn.
4.  Clone your project code onto the server.
5.  Set up the virtual environment and install dependencies from `requirements.txt`.
6.  Run the application with gunicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

## Option 2: Platform-as-a-Service (PaaS)
Services like Render or Heroku manage the servers for you, which is easier but offers less control.

### Setup on Render:
1.  Connect your GitHub repository to Render.
2.  Create a new "Web Service".
3.  Set the start command to: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
4.  Add your secret keys from the `.env` file into Render's "Environment Variables" section.