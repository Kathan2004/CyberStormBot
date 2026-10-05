# CyberStormBot

Telegram bot that served the clue and flag stages of the **CyberStorm** CTF. Players send passphrases found in earlier challenges; the bot answers with the next clue or the flag.

```
player ──"a storm is coming pirate"──► bot ──► STORM{...}
player ──"anything else"─────────────► bot ──► "Sorry, I don't understand that message."
```

## Run

```bash
cp .env.example .env                          # TELEGRAM_BOT_TOKEN from @BotFather
cp challenges.example.json challenges.json    # your passphrases and flags
pip install -r requirements.txt
python bot.py
```

Docker:

```bash
docker build -t cyberstormbot .
docker run --env-file .env -v "$PWD/challenges.json:/app/challenges.json:ro" cyberstormbot
```

Host it on a small VM or container service for the duration of the event. Do not use scheduled GitHub Actions to keep it alive: that is outside Actions' acceptable use and gets workflows disabled.

## Design

- **Configuration.** The token and the challenge map come from the environment and an untracked JSON file. Neither is in git.
- **Matching.** Passphrase matching is case- and whitespace-insensitive, and input is capped at 200 characters.
- **Polling.** `infinity_polling` reconnects on network errors and skips the backlog on restart.

## Development

```bash
pip install -r requirements-dev.txt
ruff check . && pytest -q
```
