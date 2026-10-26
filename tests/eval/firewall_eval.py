"""Scores detect_injection and redact_text over firewall_corpus.json."""
import json
import os
from collections import defaultdict

from app.callbacks import detect_injection, redact_text

CORPUS = os.path.join(os.path.dirname(__file__), "firewall_corpus.json")


def run() -> dict:
    corpus = json.load(open(CORPUS, encoding="utf-8"))

    by_cat = defaultdict(lambda: [0, 0])  # category -> [flagged, total]
    for case in corpus["injection"]:
        by_cat[case["category"]][0] += detect_injection(case["text"])
        by_cat[case["category"]][1] += 1
    injection = {cat: {"flagged": f, "total": t} for cat, (f, t) in by_cat.items()}

    pii_cat = defaultdict(lambda: [0, 0])  # category -> [redacted, total]
    for case in corpus["pii"]:
        out = redact_text(case["text"])
        for secret in case["secrets"]:
            pii_cat[case["category"]][0] += secret not in out
            pii_cat[case["category"]][1] += 1
    pii = {cat: {"redacted": r, "total": t} for cat, (r, t) in pii_cat.items()}
    return {"injection": injection, "pii": pii}


def summarize(res: dict) -> dict:
    attacks = {c: v for c, v in res["injection"].items() if not c.startswith("benign")}
    flagged = sum(v["flagged"] for v in attacks.values())
    total = sum(v["total"] for v in attacks.values())
    benign = res["injection"]["benign"]
    hard = res["injection"]["benign_hard"]
    r = sum(v["redacted"] for v in res["pii"].values())
    t = sum(v["total"] for v in res["pii"].values())
    return {
        "injection_detection_rate": flagged / total,
        "injection_miss_rate": 1 - flagged / total,
        "false_positive_rate": benign["flagged"] / benign["total"],
        "false_positive_rate_hard_negatives": hard["flagged"] / hard["total"],
        "pii_redaction_recall": r / t,
    }


if __name__ == "__main__":
    res = run()
    print(json.dumps({**res, "summary": summarize(res)}, indent=2))
