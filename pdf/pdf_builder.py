from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from pdf.pdf_layout import (
    draw_h1,
    draw_h2,
    draw_paragraph,
    draw_bullets,
)
from pdf.pdf_scorebar import (
    draw_score_bar,
    verdict_from_score,
)

def build_pdf_report(report_data: dict, output_path: str) -> None:
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    x = 50
    y = height - 50

    meta = report_data.get("meta", {})
    score_data = report_data.get("score", {})
    llm = report_data.get("llm", {})

    score_pct = int(score_data.get("overall_pct", 0))

    # -----------------------------
    # Header
    # -----------------------------
    y = draw_h1(c, x, y, "Resume ↔ Job Description Match Report")
    y = draw_paragraph(
        c,
        x,
        y,
        f"Generated: {meta.get('generated_at','')} | "
        f"Target Role: {meta.get('target_role','Not provided')} | "
        f"Seniority: {meta.get('seniority','Not specified')}",
    )

    # -----------------------------
    # At-a-glance Result
    # -----------------------------
    y = draw_h2(c, x, y, "At-a-glance Result")
    y = draw_score_bar(c, x, y, width - 100, score_pct)
    y = draw_paragraph(
        c,
        x,
        y,
        f"Verdict: {verdict_from_score(score_pct)}",
    )

    # -----------------------------
    # Match Score Explanation
    # -----------------------------
    y = draw_h2(c, x, y, "1) Match Score")
    y = draw_paragraph(c, x, y, f"Match Score: {score_pct}%")
    y = draw_paragraph(
        c,
        x,
        y,
        llm.get("summary", {}).get("score_explanation", ""),
    )

    # -----------------------------
    # Executive Summary
    # -----------------------------
    y = draw_h2(c, x, y, "2) Executive Summary")
    y = draw_paragraph(
        c,
        x,
        y,
        llm.get("summary", {}).get("overall_assessment", ""),
    )

    y = draw_h2(c, x, y, "Top Strengths")
    y = draw_bullets(
        c,
        x,
        y,
        llm.get("summary", {}).get("top_strengths", []),
    )

    y = draw_h2(c, x, y, "Top Risks")
    y = draw_bullets(
        c,
        x,
        y,
        llm.get("summary", {}).get("top_risks", []),
    )

    # -----------------------------
    # Skill Gaps
    # -----------------------------
    y = draw_h2(c, x, y, "3) Skill Gaps")
    sg = llm.get("skill_gap", {})

    y = draw_paragraph(c, x, y, "Must-have missing:")
    y = draw_bullets(
        c,
        x,
        y,
        [f"{i.get('skill')}: {i.get('how_to_add')}" for i in sg.get("must_have_missing", [])],
    )

    y = draw_paragraph(c, x, y, "Nice-to-have missing:")
    y = draw_bullets(
        c,
        x,
        y,
        [f"{i.get('skill')}: {i.get('how_to_add')}" for i in sg.get("nice_to_have_missing", [])],
    )

    y = draw_paragraph(c, x, y, "Weak signals:")
    y = draw_bullets(
        c,
        x,
        y,
        [f"{i.get('skill_or_area')}: {i.get('fix')}" for i in sg.get("weak_signals", [])],
    )

    y = draw_paragraph(c, x, y, "Priority (next 7 days):")
    y = draw_bullets(
        c,
        x,
        y,
        sg.get("priority_next_7_days", []),
    )

    # -----------------------------
    # Section-wise Feedback
    # -----------------------------
    y = draw_h2(c, x, y, "4) Section-wise Feedback")
    fb = llm.get("section_feedback", {})

    y = draw_paragraph(c, x, y, "Summary:")
    y = draw_bullets(c, x, y, fb.get("summary_feedback", []))

    y = draw_paragraph(c, x, y, "Skills:")
    y = draw_bullets(c, x, y, fb.get("skills_feedback", []))

    y = draw_paragraph(c, x, y, "Experience:")
    y = draw_bullets(c, x, y, fb.get("experience_feedback", []))

    y = draw_paragraph(c, x, y, "Projects:")
    y = draw_bullets(c, x, y, fb.get("projects_feedback", []))

    y = draw_paragraph(c, x, y, "Formatting:")
    y = draw_bullets(c, x, y, fb.get("formatting_feedback", []))

    # -----------------------------
    # Bullet Rewrites
    # -----------------------------
    y = draw_h2(c, x, y, "5) ATS-Friendly Bullet Rewrites")
    rewrites = llm.get("rewrites", {}).get("rewrites", [])

    for r in rewrites:
        y = draw_paragraph(c, x, y, "Original:")
        y = draw_bullets(c, x, y, [r.get("original", "")])
        y = draw_paragraph(c, x, y, "Rewritten:")
        y = draw_bullets(c, x, y, [r.get("rewritten", "")])
        y = draw_paragraph(c, x, y, f"Why better: {r.get('why_better','')}")

    c.showPage()
    c.save()
