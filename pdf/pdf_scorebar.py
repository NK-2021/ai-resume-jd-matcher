from reportlab.lib import colors

def draw_score_bar(c, x, y, width, score_pct):
    score_pct = max(0, min(100, int(score_pct)))

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, "Resume–JD Match Score")
    y -= 14

    bar_width = min(360, width - 120)
    bar_height = 12

    c.rect(x, y - bar_height, bar_width, bar_height)
    fill_w = bar_width * (score_pct / 100.0)
    c.setFillColor(colors.lightgrey)
    c.rect(x, y - bar_height, fill_w, bar_height, fill=1)

    c.setFillColor(colors.black)
    c.drawRightString(x + bar_width + 80, y - bar_height + 2, f"{score_pct}%")

    y -= 20
    return y

def verdict_from_score(score):
    if score >= 80:
        return "Strong fit — ready to apply."
    if score >= 60:
        return "Moderate fit — interview possible after improvements."
    return "Low fit — resume needs alignment."
