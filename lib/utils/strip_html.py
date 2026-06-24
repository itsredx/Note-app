import re
import html


def strip_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" (?=[.,!?;:])", "", text)
    return text.strip()
