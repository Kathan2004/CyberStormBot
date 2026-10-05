"""
CyberStorm CTF Telegram bot.

Replies to challenge passphrases with the next clue or the flag. Configure the
bot token and the challenge map through the environment; nothing secret lives
in the repository.

    TELEGRAM_BOT_TOKEN   token from @BotFather (required)
    CHALLENGES_FILE      JSON file mapping passphrase -> reply (default: challenges.json)
"""
import json
import logging
import os
import sys
from pathlib import Path

import telebot
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("cyberstorm")

FALLBACK = "Sorry, I don't understand that message."
MAX_INPUT = 200


def load_challenges(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise ValueError(f"{path} must be a JSON object of string -> string")
    return {normalise(k): v for k, v in data.items()}


def normalise(text: str) -> str:
    return " ".join(text.lower().split())


def reply_for(text: str, challenges: dict[str, str]) -> str:
    return challenges.get(normalise(text[:MAX_INPUT]), FALLBACK)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        sys.exit("TELEGRAM_BOT_TOKEN is not set (see .env.example)")
    challenges = load_challenges(Path(os.getenv("CHALLENGES_FILE", "challenges.json")))
    bot = telebot.TeleBot(token, parse_mode=None)

    @bot.message_handler(content_types=["text"])
    def auto_reply(message):
        answer = reply_for(message.text or "", challenges)
        log.info("chat=%s hit=%s", message.chat.id, answer != FALLBACK)
        bot.send_message(message.chat.id, answer)

    log.info("CyberStorm bot started with %d challenge(s)", len(challenges))
    bot.infinity_polling(skip_pending=True, timeout=30)


if __name__ == "__main__":
    main()
