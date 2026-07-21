"""Agent 3: Report Generator Agent."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from utils.groq_client import GroqClient

SYSTEM_PROMPT = """You are a technical report writer for software code reviews.

You will receive outputs from a Code Review Agent and a Bug Detection Agent.
Synthesize them into a polished markdown report with EXACTLY these sections:

# Code Review Report

## Project Summary
Brief overview: what the code does, scope (files/functions), and overall impression (2–4 paragraphs).

## Code Review
Summarize and organize the code review findings (readability, naming, organization, best practices).

## Potential Bugs
Summarize and organize bug detection findings (logical errors, exception handling, unused code, other bugs).

## Overall Rating
Provide a single numeric rating from 1 to 10 with brief justification.
Format exactly as: **Rating: X/10** followed by 2–3 sentences explaining the score.

Use clear markdown, bullet points where helpful, and preserve important details from both agents.
Be honest and balanced — highlight strengths as well as weaknesses."""


class ReportGeneratorAgent:
    def __init__(self, client: GroqClient) -> None:
        self.client = client

    def generate(
        self,
        project_label: str,
        code_review: str,
        bug_report: str,
        file_count: int,
    ) -> str:
        user_prompt = f"""Create a final code review report.

**Project:** {project_label}
**Files reviewed:** {file_count}
**Generated at:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

---

## Code Review Agent Output
{code_review}

---

## Bug Detection Agent Output
{bug_report}

---

Produce the complete markdown report now."""
        return self.client.chat(SYSTEM_PROMPT, user_prompt, temperature=0.2)

    def save(self, report: str, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        return output_path
