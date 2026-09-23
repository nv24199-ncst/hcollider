import json

import pytest

from hashcollider.cli import build_parser, main


def test_algorithms_command_runs(capsys):
    rc = main(["algorithms"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "sha256" in out


def test_hash_command_matches_known_value(capsys):
    rc = main(["hash", "--algorithm", "sha256", "--input", "abc"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" in out


def test_hash_command_with_weak_algorithm_warns(capsys):
    rc = main(["hash", "--algorithm", "md5", "--input", "abc"])
    err = capsys.readouterr().err
    assert rc == 0
    assert "WARNING" in err


def test_collide_command_finds_small_collision(capsys, tmp_path):
    out_path = tmp_path / "collision.json"
    rc = main([
        "collide", "--algorithm", "sha256", "--bits", "8",
        "--generator", "sequential", "--length", "16",
        "--output", str(out_path),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Collision found" in out
    assert out_path.exists()
    data = json.loads(out_path.read_text())
    assert data["effective_bits"] == 8


def test_collide_command_rejects_excessive_bits_without_override(capsys):
    rc = main(["collide", "--algorithm", "sha256", "--bits", "40"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "safety limit" in err or "Error" in err


def test_collide_command_rejects_invalid_algorithm():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["collide", "--algorithm", "not-real", "--bits", "8"])


def test_collide_command_rejects_invalid_bits(capsys):
    rc = main(["collide", "--algorithm", "sha256", "--bits", "0"])
    assert rc == 1


def test_benchmark_command_runs(capsys):
    rc = main(["benchmark", "--algorithm", "sha256", "--bits", "8", "--iterations", "2"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Hashes/sec" in out


def test_verify_command_on_missing_file(capsys):
    rc = main(["verify", "/tmp/does-not-exist-hashcollider.json"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "does not exist" in err


def test_verify_and_report_full_flow(capsys, tmp_path):
    out_path = tmp_path / "collision.json"
    main([
        "collide", "--algorithm", "sha256", "--bits", "8",
        "--generator", "sequential", "--output", str(out_path),
    ])
    capsys.readouterr()

    rc = main(["verify", str(out_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PASS" in out

    report_path = tmp_path / "report.md"
    rc = main(["report", str(out_path), "--output", str(report_path)])
    capsys.readouterr()
    assert rc == 0
    assert report_path.exists()
    assert "HashCollider Collision Report" in report_path.read_text()


def test_explain_command(capsys):
    rc = main(["explain", "collision"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "birthday" in out.lower()


def test_no_command_shows_error():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])
