from pdf.pdf_utils import wrap_text

def draw_h1(c, x, y, text):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, text)
    return y - 26

def draw_h2(c, x, y, text):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, text)
    return y - 18

def draw_paragraph(c, x, y, text, max_chars=95):
    c.setFont("Helvetica", 10)
    for line in wrap_text(text, max_chars):
        if y < 60:
            c.showPage()
            y = 800
        c.drawString(x, y, line)
        y -= 12
    return y - 6

def draw_bullets(c, x, y, items, max_chars=92):
    c.setFont("Helvetica", 10)
    for it in items or []:
        for i, line in enumerate(wrap_text(it, max_chars)):
            prefix = "• " if i == 0 else "  "
            if y < 60:
                c.showPage()
                y = 800
            c.drawString(x, y, prefix + line)
            y -= 12
    return y - 6
