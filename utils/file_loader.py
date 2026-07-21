"""Load Python source files from a path (file or directory)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SourceFile:
    path: Path
    content: str


def load_python_sources(target: str | Path) -> list[SourceFile]:
    """Load one .py file or all .py files under a directory."""
    path = Path(target).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if path.is_file():
        if path.suffix != ".py":
            raise ValueError(f"Expected a .py file, got: {path}")
        return [_read_file(path)]

    if path.is_dir():
        files = sorted(path.rglob("*.py"))
        if not files:
            raise ValueError(f"No Python files found in: {path}")
        return [_read_file(f) for f in files]

    raise ValueError(f"Invalid path: {path}")


def _read_file(path: Path) -> SourceFile:
    content = path.read_text(encoding="utf-8")
    return SourceFile(path=path, content=content)


def format_sources_for_prompt(sources: list[SourceFile]) -> str:
    """Combine multiple source files into a single prompt block."""
    blocks: list[str] = []
    for source in sources:
        relative = source.path.name
        blocks.append(f"### File: {relative}\n```python\n{source.content}\n```")
    return "\n\n".join(blocks)


def get_project_label(sources: list[SourceFile]) -> str:
    """Human-readable label for the reviewed target."""
    if len(sources) == 1:
        return str(sources[0].path)
    parent = sources[0].path.parent
    return f"{parent} ({len(sources)} files)"
