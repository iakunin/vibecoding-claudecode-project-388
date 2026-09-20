#!/usr/bin/env python3
"""Отправляет текст в Telegram. Только стандартная библиотека.

Запуск:
    python3 send.py "текст сообщения"

Токен и chat id берутся из переменных окружения TELEGRAM_BOT_TOKEN и
TELEGRAM_CHAT_ID, а если их там нет — из файла .env рядом со скриптом.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.telegram.org/bot{token}/sendMessage"


def load_env():
    """Дописывает в окружение значения из .env, не затирая уже заданные."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def send(text):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit("Нет TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID: задайте их в окружении или в .env")

    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": "true",
    }).encode()

    try:
        with urllib.request.urlopen(API.format(token=token), data=data, timeout=20) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as e:
        # Телеграм кладёт причину отказа в тело ответа, а не в код статуса.
        detail = json.load(e).get("description", e.reason)
        sys.exit(f"Telegram отказал: HTTP {e.code} — {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Не достучались до Telegram: {e.reason}")

    if not body.get("ok"):
        sys.exit(f"Telegram отказал: {body.get('description')}")
    print("Отправлено.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        sys.exit('Нужен ровно один аргумент — текст сообщения: python3 send.py "текст"')
    load_env()
    send(sys.argv[1])
