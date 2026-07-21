#!/usr/bin/env python3
"""Multi-Agent Code Reviewer – CLI entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agents.bug_detection_agent import BugDetectionAgent
from agents.code_review_agent import CodeReviewAgent
from agents.report_generator_agent import ReportGeneratorAgent
from utils.file_loader import (
    format_sources_for_prompt,
    get_project_label,
    load_python_sources,
)
from utils.groq_client import GroqClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multi-Agent Python Code Reviewer powered by Groq LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py sample_code/calculator.py
  python main.py sample_code/
  python main.py my_project/ -o review_output/report.md
        """,
    )
    parser.add_argument(
        "target",
        help="Path to a Python file (.py) or folder containing Python files",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="report.md",
        help="Output path for the generated report (default: report.md)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Groq model name (overrides GROQ_MODEL env var)",
    )
    return parser.parse_args()


def run_review(target: str, output: str, model: str | None = None) -> Path:
    print(f"Loading source from: {target}")
    sources = load_python_sources(target)
    project_label = get_project_label(sources)
    code_block = format_sources_for_prompt(sources)
    print(f"Found {len(sources)} Python file(s)\n")

    client = GroqClient(model=model)
    print(f"Using model: {client.model}\n")

    review_agent = CodeReviewAgent(client)
    bug_agent = BugDetectionAgent(client)
    report_agent = ReportGeneratorAgent(client)

    print("Agent 1 – Code Review Agent: analyzing readability, naming, organization...")
    code_review = review_agent.review(code_block, project_label)
    print("  Done.\n")

    print("Agent 2 – Bug Detection Agent: scanning for logical errors and bugs...")
    bug_report = bug_agent.detect(code_block, project_label)
    print("  Done.\n")

    print("Agent 3 – Report Generator: synthesizing final report...")
    report = report_agent.generate(
        project_label=project_label,
        code_review=code_review,
        bug_report=bug_report,
        file_count=len(sources),
    )
    output_path = Path(output)
    report_agent.save(report, output_path)
    print(f"  Done.\n")

    print(f"Report saved to: {output_path.resolve()}")
    return output_path


def main() -> int:
    args = parse_args()
    try:
        run_review(args.target, args.output, args.model)
        return 0
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
