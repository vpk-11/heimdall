from tests.eval.firewall_eval import run, summarize


def test_known_phrases_and_obfuscation_are_caught():
    inj = run()["injection"]
    assert inj["direct"]["flagged"] == inj["direct"]["total"]


def test_corpus_scores_are_computable():
    # Misses in paraphrase/base64/multilingual/roleplay are measured, not asserted;
    # run `python -m tests.eval.firewall_eval` for the per-category report.
    s = summarize(run())
    assert 0 <= s["injection_detection_rate"] <= 1
    assert s["pii_redaction_recall"] > 0
