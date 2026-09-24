"""Normalization applied to BOTH reference and hypothesis before WER/CER.
Derja has no standard spelling, so we remove the differences that don't change meaning."""
import re
import unicodedata

_DIACRITICS = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")


def normalize(text: str) -> str:
    t = unicodedata.normalize("NFKC", text or "")
    t = t.replace("\u0640", "")              # tatweel
    t = _DIACRITICS.sub("", t)               # tashkeel
    t = re.sub("[أإآٱ]", "ا", t)             # alef variants
    t = t.replace("ى", "ي").replace("ة", "ه")
    t = t.translate(_DIGITS)                 # Arabic-Indic digits -> ASCII
    t = t.lower()
    t = re.sub(r"[^\w\s]", " ", t)           # punctuation / apostrophes -> space
    t = t.replace("_", " ")
    return re.sub(r"\s+", " ", t).strip()
