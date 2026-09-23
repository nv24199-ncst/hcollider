from hashcollider.reports.generator import generate_report


def _sample_data():
    return {
        "algorithm": "sha256",
        "effective_bits": 16,
        "generator": "sequential",
        "input_a": "aabbcc",
        "input_b": "ddeeff",
        "hash_a": "abcd" * 16,
        "hash_b": "abcd" * 16,
        "truncated_hash": "abcd",
        "attempts": 300,
        "elapsed_seconds": 0.01,
        "hashes_per_second": 30000,
    }


def test_report_contains_key_sections():
    report = generate_report(_sample_data())
    assert "# HashCollider Collision Report" in report
    assert "sha256" in report
    assert "aabbcc" in report
    assert "ddeeff" in report
    assert "This is not a collision in the full sha256 algorithm" in report or \
           "not a collision in the full" in report


def test_report_explains_limitation_clearly():
    report = generate_report(_sample_data())
    assert "16-bit truncated" in report or "16 bits" in report
    assert "Limitations" in report
