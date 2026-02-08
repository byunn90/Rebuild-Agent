🧠 AI-Agent

An experimental AI-powered command-line agent built with Python and Google’s Gemini API, inspired by the Boot.dev Build an AI Agent course.

This project explores how command-driven AI agents can plan, reason, and execute real local actions instead of acting as a simple chatbot. The agent follows explicit user instructions to generate files, create code, inspect directories, and assist with debugging — all while enforcing strict security guardrails.

🚀 Features
🔹 Gemini API Integration

Uses Google’s google-genai client for reasoning, planning, and content generation.

🔹 Command-Driven Agent (Not a Chatbot)

Responds only to explicit commands

Converts instructions into concrete actions such as:

File creation

Code generation

Analysis and explanations

🔹 Local File & Directory Interaction

The agent can:

Read files

List directories

Create new files with strict formatting rules

Generate structured documents and code outputs

🔹 Bug Assistance & Debugging Support

Helps analyze errors

Suggests fixes based on user-provided context and instructions

🔹 Secure Configuration via Environment Variables

API keys are loaded using .env

Secrets are excluded from version control to prevent leaks

🛠️ Example Usage

Run the agent from the command line with a clear instruction:

uv run main.py "Create a Python script that validates user input and explains each step"


Or ask for analysis/debugging help:

uv run main.py "Explain why this Python function raises a KeyError and how to fix it"


The agent produces real, usable outputs, not just conversational responses.

🔐 Security & Guardrails

Secrets are stored in environment variables (.env)

Explicit execution boundaries are enforced

No unrestricted command execution

Designed to prevent accidental or unsafe system operations

This project intentionally prioritizes safety and control over unrestricted autonomy.

🧪 What I’m Exploring With This Project

Using LLMs as task-oriented agents

Translating natural language instructions into deterministic system actions

Designing guardrails for local AI execution

Combining AI-assisted workflows with traditional software engineering practices

📚 Learning Context

This project was built alongside my ongoing focus on computer science fundamentals, particularly data structures and algorithms, through Boot.dev.
The goal is to pair hands-on AI projects with a strong backend and problem-solving foundation.

⚠️ Disclaimer

This is an experimental learning project and not intended for production use. APIs, prompts, and execution logic may change as the project evolves.