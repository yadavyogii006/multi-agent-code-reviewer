"""Agent 2: Bug Detection Agent."""

from __future__ import annotations

from utils.groq_client import GroqClient

SYSTEM_PROMPT = """You are an expert Python debugger and static analysis specialist.

Analyze the provided Python code and identify potential bugs and issues:
1. **Logical Errors** – incorrect conditions, off-by-one, wrong operators
2. **Missing Exception Handling** – unhandled failures, bare except, swallowed errors
3. **Unused Variables / Dead Code** – unused imports, unreachable code
4. **Potential Bugs** – race conditions, resource leaks, type mismatches, security issues

Be specific: cite file names and approximate line numbers.
For each issue include: severity ([Critical]/[High]/[Medium]/[Low]), description, and a suggested fix.
If no issues are found in a category, state that clearly."""


class BugDetectionAgent:
    def __init__(self, client: GroqClient) -> None:
        self.client = client

    def detect(self, code_block: str, project_label: str) -> str:
        user_prompt = f"""Analyze the following Python project for bugs: **{project_label}**

{code_block}

List all potential bugs and issues now."""
        return self.client.chat(SYSTEM_PROMPT, user_prompt)
