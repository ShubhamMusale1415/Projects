import re

def detect_title(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return "Untitled"

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()
