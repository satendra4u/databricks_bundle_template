"""Generic AI tool functions for {{.project_name}}.

Add your domain-specific tools here. Each function should accept JSON-like inputs and return JSON-like outputs.
"""
from typing import Any, Dict


def {{.tool_name}}(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Example generic tool.

    Parameters
    ----------
    payload: dict
        Example input: {"text": "hello"}
    Returns
    -------
    dict
        Example output: {"echo": "hello"}
    """
    text = payload.get("text", "")
    return {"echo": text}
