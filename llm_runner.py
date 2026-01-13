from __future__ import annotations
from typing import Callable, Dict

from ollama_client import ollama_chat, extract_json_first
from llm_prompts import (
    prompt_score_and_summary,
    prompt_skill_gap,
    prompt_section_feedback,
    prompt_rewrite_bullets,
)


def run_llm_bundle(
    model: str,
    resume_text: str,
    jd_text: str,
    numeric_score: int,
    target_role: str,
    seniority: str,
    log: Callable[[str], None],
) -> Dict:
    """
    Runs all LLM calls and returns a merged dict.
    """
    # Keep deterministic for JSON reliability + speed
    temperature = 0.0

    log("  - LLM 1/4: Executive summary...")
    summary_txt = ollama_chat(
        model,
        prompt_score_and_summary(resume_text, jd_text, numeric_score, target_role, seniority),
        temperature=temperature,
    )
    summary = extract_json_first(summary_txt)

    log("  - LLM 2/4: Skill gap analysis...")
    skill_gap_txt = ollama_chat(
        model,
        prompt_skill_gap(resume_text, jd_text),
        temperature=temperature,
    )
    skill_gap = extract_json_first(skill_gap_txt)

    log("  - LLM 3/4: Section-wise feedback...")
    section_fb_txt = ollama_chat(
        model,
        prompt_section_feedback(resume_text, jd_text),
        temperature=temperature,
    )
    section_feedback = extract_json_first(section_fb_txt)

    log("  - LLM 4/4: Bullet rewrites...")
    rewrites_txt = ollama_chat(
        model,
        prompt_rewrite_bullets(resume_text, jd_text, max_bullets=6),
        temperature=temperature,
    )
    rewrites = extract_json_first(rewrites_txt)

    return {
        "summary": summary,
        "skill_gap": skill_gap,
        "section_feedback": section_feedback,
        "rewrites": rewrites,
    }
