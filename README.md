# Multi-Agent Code Reviewer

A Python CLI tool that uses **three LLM-powered agents** (via [GroqCloud](https://console.groq.com)) to review Python source code and produce a structured markdown report.

## Overview

| Agent | Role |
|-------|------|
| **Agent 1 – Code Review** | Readability, naming conventions, function organization, best practices |
| **Agent 2 – Bug Detection** | Logical errors, missing exception handling, unused variables, potential bugs |
| **Agent 3 – Report Generator** | Combines both outputs into `report.md` with summary, findings, and rating (1–10) |

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  Python file(s) │────▶│  Agent 1: Code Review │────▶│                     │
└─────────────────┘     └──────────────────────┘     │  Agent 3: Report    │──▶ report.md
         │                ┌──────────────────────┐     │  Generator          │
         └───────────────▶│  Agent 2: Bug Detect │────▶│                     │
                          └──────────────────────┘     └─────────────────────┘
                                    ▲
                                    │
                          ┌─────────┴─────────┐
                          │   Groq LLM API    │
                          └───────────────────┘
```

## Features

- Accepts a single `.py` file or a folder of Python files
- Three specialized agents with focused system prompts
- Generates a polished `report.md` with Project Summary, Code Review, Potential Bugs, and Overall Rating
- Configurable Groq model via environment variable
- Sample code included for quick testing

## Prerequisites

- Python 3.10+
- A [GroqCloud API key](https://console.groq.com/keys) (free tier available)

## Installation

```bash
git clone https://github.com/yadavyogii006/multi-agent-code-reviewer.git
cd multi-agent-code-reviewer

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

Copy the example env file and add your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

## Usage

Review a single file:

```bash
python main.py sample_code/calculator.py
```

Review an entire folder:

```bash
python main.py sample_code/
```

Custom output path:

```bash
python main.py sample_code/ -o reviews/my_report.md
```

Override the model:

```bash
python main.py sample_code/calculator.py --model llama-3.1-8b-instant
```

## Sample Output

The tool writes `report.md` with sections like:

```markdown
# Code Review Report

## Project Summary
...

## Code Review
- [Major] Function `calc` lacks type hints and docstring
- [Minor] Class name `dataProcessor` should be `DataProcessor` (PEP 8)
...

## Potential Bugs
- [Critical] Division by zero in `calc()` when op is "div"
- [High] Off-by-one error in `process_numbers()` loop
...

## Overall Rating
**Rating: 4/10**
...
```

## Project Structure

```
.
├── main.py                      # CLI entry point
├── agents/
│   ├── code_review_agent.py     # Agent 1
│   ├── bug_detection_agent.py   # Agent 2
│   └── report_generator_agent.py # Agent 3
├── utils/
│   ├── file_loader.py           # Load .py files / directories
│   └── groq_client.py           # Groq API wrapper
├── sample_code/                 # Demo code with intentional issues
├── .env.example
├── requirements.txt
└── README.md
```

## Project Outcomes

After running the reviewer on the included sample code, you can expect:

1. **Actionable code review feedback** — naming, structure, and PEP 8 suggestions
2. **Bug identification** — off-by-one loops, missing error handling, resource leaks
3. **Consolidated report** — single markdown document suitable for sharing with a team
4. **Quantitative score** — 1–10 overall rating with justification

## Tech Stack

- **Python 3.10+**
- **Groq SDK** — fast LLM inference via GroqCloud
- **python-dotenv** — environment variable management

## Limitations

- LLM output may vary between runs; treat findings as suggestions, not guarantees
- Very large codebases may exceed token limits — review smaller modules or folders
- Requires an active internet connection and valid Groq API key

## License

MIT

## Author

Built as a multi-agent code review assignment using GroqCloud LLM APIs.
