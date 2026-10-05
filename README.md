Markdown


# Telegram Utility Bot (No Dependencies)

A lightweight multi-functional Telegram bot written in **pure Python** using only standard built-in libraries (`urllib`, `json`, `ast`). No `pip install` or external frameworks required!

---

## ⚡ Features

* **🧮 Safe Math Calculator:** Evaluates mathematical expressions using AST parsing safely (supports `+`, `-`, `*`, `/`, `**`, `%`, and parentheses).
* **🔑 Secure Password Generator:** Creates cryptographically safe random passwords of customizable length (8–64 characters).
* **🎲 Utility Commands:** Includes coin flip (`/coin`), dice roll (`/dice`), and random number generator (`/random`).
* **🕒 Time & Date:** Displays current system time and date.
* **🌐 Zero Dependencies:** Built strictly using Python's standard library. Runs out of the box.

---

## 🛠️ Built-In Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `/start` | Welcome message & command overview | `/start` |
| `/help` | List available commands | `/help` |
| `/calc <expr>` | Calculate math expression safely | `/calc 2+2*(3+4)` |
| `/password <len>`| Generate secure password | `/password 16` |
| `/random <min> <max>` | Random integer in range | `/random 1 100` |
| `/coin` | Flip a coin (Heads/Tails) | `/coin` |
| `/dice` | Roll a standard 6-sided die | `/dice` |
| `/time` | Show current date and time | `/time` |

---

## 🚀 Quick Start

### 1. Obtain a Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the instructions to create your bot.
3. Copy your **HTTP API Token**.

### 2. Run the Bot

#### Option A: Set Environment Variable (Recommended)
**Linux / macOS:**
```bash
export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
python 3_telegram_bot.py
Windows (CMD):

DOS


set TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
python 3_telegram_bot.py
Windows (PowerShell):

PowerShell


$env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
python 3_telegram_bot.py
Option B: Direct Input
Run the script directly, and it will prompt you to enter your token:

Bash


python 3_telegram_bot.py
🔒 Security
Unlike scripts using eval(), this bot parses mathematical expressions into an Abstract Syntax Tree (AST) using Python's ast module. It explicitly filters allowed operations and prevents arbitrary code execution or memory exhaustion.

📋 Requirements
Python 3.8+

No third-party packages needed!

📄 License
This project is licensed under the MIT License — feel free to use, modify, and distribute it!
