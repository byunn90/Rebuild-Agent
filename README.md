# 🧠 AI-Agent

An experimental **AI-powered command-line agent** built with **Python** and Google’s **Gemini API**, inspired by the Boot.dev *Build an AI Agent* course.

This project explores how **command-driven AI agents** can plan, reason, and execute **real local actions** instead of acting as a simple chatbot. The agent follows explicit user instructions to generate files, create code, inspect directories, and assist with debugging — all while enforcing strict security guardrails.

---

## 🚀 Features

- **Gemini API Integration**
  - Uses Google’s `google-genai` client for reasoning, planning, and content generation.

- **Command-Driven Agent (Not a Chatbot)**
  - Responds only to explicit commands.
  - Converts instructions into concrete actions such as file creation, code generation, and analysis.

- **Local File & Directory Interaction**
  - Read files  
  - List directories  
  - Create new files with strict formatting rules  
  - Generate structured documents and code outputs  
  - Has calculator function
  - Fixes live bugs (Must give it direct instructions where the bug is which directory)
  - Creates it own files on input

- **Bug Assistance & Debugging Support**
  - Helps analyze errors and suggests fixes based on user-provided context and instructions.

- **Secure Configuration via Environment Variables**
  - API keys are loaded using `.env`.
  - Secrets are excluded from version control to prevent leaks.

---

## 🛠️ Example Usage

Run the agent from the command line with a clear instruction:

```bash
uv run main.py "Create a Python script that validates user input and explains each step"
