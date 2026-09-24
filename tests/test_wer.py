from eval.stt_bench import summarize
from eval.text_norm import normalize


def test_arabic_normalization():
    assert normalize("عَسْلامة") == normalize("عسلامه")
    assert normalize("أحب") == normalize("احب")
    assert normalize("رقم ٦٠٤٢٨١") == "رقم 604281"


def test_french_and_punctuation():
    assert normalize("Fuite d'eau, Rue de la Liberté!") == "fuite d eau rue de la liberté"


def test_summary_wer():
    rows = [{"provider": "p", "condition": "c", "id": "1", "intent": "x",
             "ref": "a b c d", "hyp": "a b c", "latency_ms": 100.0, "error": ""}]
    s = summarize(rows)[0]
    assert s["WER"] == 0.25 and s["errors"] == 0
