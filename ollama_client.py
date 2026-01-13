from __future__ import annotations
import subprocess
import json
import re

def ollama_chat(model: str, messages: list[dict], temperature: float = 0.0) -> str:
    """
    Runs a local Ollama model and returns raw text output.
    Works fully offline.
    """
    prompt = _stitch_messages(messages)

    cmd = ["ollama", "run", model]

    result = subprocess.run(
        cmd,
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Ollama failed: {result.stderr.decode('utf-8', errors='ignore')}"
        )

    return result.stdout.decode("utf-8", errors="ignore").strip()

def extract_json_first(text: str) -> dict:
    """
    Safely extracts FIRST JSON object from LLM output.
    Also sanitizes invalid control characters.
    """

    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in LLM output.")

    # Take substring starting from first {
    s = text[start:]

    # 🔴 CRITICAL FIX: remove illegal control characters
    s = re.sub(r'[\x00-\x1F\x7F]', '', s)

    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(s)
    return obj



def _stitch_messages(messages: list[dict]) -> str:
    parts = []
    for m in messages:
        role = m.get("role", "user").upper()
        content = m.get("content", "")
        parts.append(f"{role}:\n{content}\n")
    return "\n".join(parts).strip()
