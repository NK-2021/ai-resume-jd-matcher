def prompt_score_and_summary(resume_text: str, jd_text: str, numeric_score: int, target_role: str, seniority: str) -> list[dict]:
    return [
        {"role": "system", "content": (
            "You are a strict resume evaluator. "
            "Return ONLY valid JSON. No markdown, no commentary."
        )},
        {"role": "user", "content": f"""
TASK:
Create an executive summary for a Resume ↔ Job Description match report.

INPUTS:
- Target role: {target_role or "Not provided"}
- Seniority: {seniority}
- Similarity score (0-100) from embeddings: {numeric_score}

RESUME (TEXT):
{resume_text}

JOB DESCRIPTION (TEXT):
{jd_text}

OUTPUT JSON SCHEMA (return ONLY this JSON):
{{
  "headline": "string (max 12 words)",
  "overall_assessment": "string (2-4 sentences, professional)",
  "top_strengths": ["string", "string", "string"],
  "top_risks": ["string", "string", "string"],
  "score_explanation": "string (1-2 sentences explaining what the score reflects)"
}}

RULES:
- Do NOT invent experience. If missing, say it's missing.
- Be direct and practical.
"""}
    ]


def prompt_skill_gap(resume_text: str, jd_text: str) -> list[dict]:
    return [
        {"role": "system", "content": "Extract skill gaps. Return ONLY valid JSON."},
        {"role": "user", "content": f"""
TASK:
Identify missing skills and weak areas in the resume compared to the JD.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

OUTPUT JSON (ONLY):
{{
  "must_have_missing": [{{"skill":"string","why_it_matters":"string","how_to_add":"string"}}],
  "nice_to_have_missing": [{{"skill":"string","why_it_matters":"string","how_to_add":"string"}}],
  "weak_signals": [{{"skill_or_area":"string","issue":"string","fix":"string"}}],
  "priority_next_7_days": ["string", "string", "string"]
}}

RULES:
- Keep items concrete (skills/tools/domain keywords).
- If a skill is present but weak (no evidence), put it in weak_signals.
"""}
    ]


def prompt_section_feedback(resume_text: str, jd_text: str) -> list[dict]:
    return [
        {"role": "system", "content": "Give section-wise resume feedback. Return ONLY valid JSON."},
        {"role": "user", "content": f"""
TASK:
Give section-wise feedback to improve ATS + recruiter clarity.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

OUTPUT JSON (ONLY):
{{
  "summary_feedback": ["string","string","string"],
  "skills_feedback": ["string","string","string"],
  "experience_feedback": ["string","string","string"],
  "projects_feedback": ["string","string","string"],
  "formatting_feedback": ["string","string","string"]
}}

RULES:
- Actionable, not generic.
- Mention missing metrics, missing keywords, unclear impact, poor structure.
"""}
    ]


def prompt_rewrite_bullets(resume_text: str, jd_text: str, max_bullets: int = 6) -> list[dict]:
    return [
        {"role": "system", "content": "Rewrite bullets to be ATS-friendly. Return ONLY valid JSON."},
        {"role": "user", "content": f"""
TASK:
Pick up to {max_bullets} bullets from the resume experience/projects that are weak or generic.
Rewrite them to be ATS-friendly and impact-focused.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

OUTPUT JSON (ONLY):
{{
  "rewrites": [
    {{
      "original": "string",
      "rewritten": "string",
      "why_better": "string (one sentence)"
    }}
  ]
}}

RULES:
- Do not invent tools or achievements. If metrics are missing, use safe framing like
  "improved", "reduced", "optimized" without fake numbers.
- Keep rewritten bullets 1 line if possible.
"""}
    ]
