# utils.py
import re


def detect_title(text):
    # First non-empty line is treated as the title
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return "Untitled"


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()