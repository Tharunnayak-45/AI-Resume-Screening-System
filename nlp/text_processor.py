import re


def clean_text(text):
    """
    Convert text to lowercase and remove unnecessary characters.
    """

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()