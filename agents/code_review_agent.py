"""Agent 1: Code Review Agent."""

from __future__ import annotations

from utils.groq_client import GroqClient

SYSTEM_PROMPT = """You are an expert Python code reviewer focused on code quality and maintainability.

Analyze the provided Python code and produce a structured review covering:
1. **Code Readability** – clarity, comments, formatting, complexity
2. **Naming Conventions** – variables, functions, classes (PEP 8)
3. **Function Organization** – single responsibility, modularity, cohesion
4. **General Best Practices** – PEP 8, DRY, type hints, docstrings, design patterns

Be specific: cite file names and line references when possible.
Use markdown with bullet points and severity tags: [Critical], [Major], [Minor], [Suggestion].
If a section has no issues, say so briefly."""


class CodeReviewAgent:
    def __init__(self, client: GroqClient) -> None:
        self.client = client

    def review(self, code_block: str, project_label: str) -> str:
        user_prompt = f"""Review the following Python project: **{project_label}**

{code_block}

Provide your code review now."""
        return self.client.chat(SYSTEM_PROMPT, user_prompt)
