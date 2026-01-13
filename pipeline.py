from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from extract import extract_text_from_uploaded_file, clean_text
from scoring import score_resume_vs_jd
from pdf.pdf_builder import build_pdf_report

from llm_runner import run_llm_bundle


DEFAULT_OLLAMA_MODEL = "mistral:7b"  # change to "llama3.1:8b" if you want

def _make_preview(report_data: dict) -> dict:
    score_pct = int(report_data.get("score", {}).get("overall_pct", 0))
    llm = report_data.get("llm", {})

    verdict = _verdict_from_score(score_pct)

    strengths = (llm.get("summary", {}).get("top_strengths", []) or [])[:3]
    risks = (llm.get("summary", {}).get("top_risks", []) or [])[:3]

    # From skill gap section: pick top 3 next actions (priority)
    actions = (llm.get("skill_gap", {}).get("priority_next_7_days", []) or [])[:3]

    return {
        "score_pct": score_pct,
        "verdict": verdict,
        "strengths": strengths,
        "gaps": risks,          # show risks as "gaps" in UI
        "actions": actions,
    }

def _verdict_from_score(score_pct: int) -> str:
    if score_pct >= 75:
        verdict = "Strong fit — ready to apply."
    elif score_pct >= 55:
        verdict = "Moderate fit — interview possible with improvements."
    else:
        verdict = "Low fit — resume needs alignment to this job."
    return verdict
    # if score_pct >= 80:
    #     return "Strong fit — ready to apply. Minor improvements recommended."
    # if score_pct >= 60:
    #     return "Moderate fit — interview possible after targeted improvements."
    # return "Low fit — resume needs alignment to this job description."


def generate_report(
    resume_file,
    resume_text: str,
    jd_text: str,
    target_role: str = "",
    seniority: str = "Not specified",
    ui_log=None,
    model: str = DEFAULT_OLLAMA_MODEL,
) -> str:
    """
    Orchestrates: extract -> clean -> score -> LLM analysis -> PDF.
    Returns: output PDF path.
    """

    def log(msg: str):
        # Visible in terminal
        print(msg, flush=True)
        # Visible in Streamlit UI (if provided)
        if ui_log is not None:
            try:
                ui_log.write(msg)
            except Exception:
                pass

    log("STEP 1/5: Extracting + cleaning text...")

    extracted = extract_text_from_uploaded_file(resume_file) if resume_file is not None else ""
    resume_raw = resume_text.strip() if (resume_text and resume_text.strip()) else extracted

    resume = clean_text(resume_raw)
    jd = clean_text(jd_text)

    if not resume:
        raise ValueError("Resume text is empty after extraction. Try pasting resume text instead of PDF.")
    if not jd:
        raise ValueError("Job Description text is empty.")

    # Trim big inputs before LLM (major speed improvement)
    resume_for_llm = _trim_for_llm(resume, max_chars=12000)
    jd_for_llm = _trim_for_llm(jd, max_chars=12000)

    log("STEP 2/5: Computing match score (MiniLM embeddings)...")
    score = score_resume_vs_jd(resume, jd)
    numeric_score = score["overall_pct"]
    log(f"✓ Match score: {numeric_score}%")

    log("STEP 3/5: Running LLM analysis (Ollama)...")
    llm_outputs = run_llm_bundle(
        model=model,
        resume_text=resume_for_llm,
        jd_text=jd_for_llm,
        numeric_score=numeric_score,
        target_role=target_role,
        seniority=seniority,
        log=log,
    )

    report_data = {
        "meta": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "target_role": target_role or "Not provided",
            "seniority": seniority,
            "model": model,
        },
        "score": score,
        "llm": llm_outputs,
    }

    log("STEP 4/5: Building PDF...")
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    filename = f"Resume_JD_Match_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = out_dir / filename

    build_pdf_report(report_data, str(output_path))

    log("STEP 5/5: Done ✅")

    preview = _make_preview(report_data)
    return str(output_path), preview


def _trim_for_llm(text: str, max_chars: int = 12000) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    # keep start + end (end often contains recent experience / education)
    head = text[: int(max_chars * 0.7)]
    tail = text[-int(max_chars * 0.3) :]
    return head + "\n...\n" + tail

def build_preview(report_data: dict) -> dict:
    score_pct = int(report_data.get("score", {}).get("overall_pct", 0))
    llm = report_data.get("llm", {})

    summary = llm.get("summary", {})
    sg = llm.get("skill_gap", {})

    strengths = (summary.get("top_strengths", []) or [])[:3]
    risks = (summary.get("top_risks", []) or [])[:3]

    must_missing = sg.get("must_have_missing", []) or []
    must_missing = [f"{x.get('skill','')}: {x.get('why_it_matters','')}".strip(": ") for x in must_missing][:3]

    next7 = (sg.get("priority_next_7_days", []) or [])[:3]

    verdict = _verdict_from_score(score_pct)

    return {
        "score_pct": score_pct,
        "verdict": verdict,
        "strengths": strengths,
        "risks": risks,
        "must_missing": must_missing,
        "next_7_days": next7,
    }


def _verdict_from_score(score_pct: int) -> str:
    if score_pct >= 80:
        return "Strong fit — ready to apply. Minor improvements recommended."
    if score_pct >= 60:
        return "Moderate fit — interview possible after targeted improvements."
    return "Low fit — resume needs alignment to this job description."

