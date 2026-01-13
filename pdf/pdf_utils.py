def wrap_text(text: str, max_chars: int):
    text = (text or "").replace("\r", " ").replace("\n", " ")
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
