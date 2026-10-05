import json

import pytest

import bot


@pytest.fixture
def challenges(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"Aye Aye  Captain": "clue", "a storm is coming pirate": "FLAG"}))
    return bot.load_challenges(p)


def test_match_is_case_and_whitespace_insensitive(challenges):
    assert bot.reply_for("  AYE aye   captain ", challenges) == "clue"


def test_unknown_message_gets_fallback(challenges):
    assert bot.reply_for("give me the flag", challenges) == bot.FALLBACK


def test_oversized_input_is_truncated(challenges):
    assert bot.reply_for("a" * 10_000, challenges) == bot.FALLBACK


def test_invalid_challenge_file_rejected(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("[1, 2]")
    with pytest.raises(ValueError):
        bot.load_challenges(p)
