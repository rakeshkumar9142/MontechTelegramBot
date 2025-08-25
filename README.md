Montech Telegram Bot
====================

A clean, modular Telegram bot for Montech using python-telegram-bot (v21+). It supports:

- /start: Welcome message and brief intro
- /about: About Montech
- /services: List of services
- /contact: Collects name, email, and message, stores in contacts.csv

Project structure
-----------------

```
MontechTelegramBot/
  app/
    __init__.py
    main.py
    config.py
    handlers/
      __init__.py
      start.py
      about.py
      services.py
      contact.py
    storage/
      __init__.py
      contacts.py
  .env.example
  requirements.txt
  README.md
```

Prerequisites
-------------

- Python 3.10+
- A Telegram Bot token from BotFather

Quick start (local)
-------------------

1) Create and activate a virtual environment

Windows PowerShell:
```
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Configure environment

- Copy `.env.example` to `.env`
- Set `TELEGRAM_BOT_TOKEN="<your-token>"`

4) Run the bot
```
python -m app.main
```

Bot commands
------------

Register commands with BotFather (optional for menu):

```
start - Start interacting with Montech bot
about - About Montech
services - Our services
contact - Send your contact details
```

Deployment notes
----------------

Render:
- Create a Web Service (or Background Worker) from this repo
- Environment: add `TELEGRAM_BOT_TOKEN`
- Start command: `python -m app.main`

Hostinger / generic VPS:
- Ensure Python 3.10+, create venv, install `requirements.txt`
- Export env var `TELEGRAM_BOT_TOKEN`
- Use `tmux`/`screen` or a process manager (e.g., `pm2`, `supervisor`, `systemd`) to keep the bot running

Security
--------

- Do not commit your real token. Use `.env` locally and provider secrets in production
- Rotate the token in BotFather if it leaks

Editing copy
------------

You can edit texts in the handler modules under `app/handlers/`.
