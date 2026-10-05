"""Telegram-бот (без сторонних библиотек, только стандартный Python).

Как запустить:
  1. В Telegram найдите @BotFather, отправьте /newbot и получите токен.
  2. Запустите программу и вставьте токен (или задайте переменную
     окружения TELEGRAM_BOT_TOKEN).
  3. Откройте своего бота в Telegram и напишите /start.

Команды: /start /help /coin /dice /random /password /calc /time
"""

from __future__ import annotations

import ast
import json
import operator
import os
import random
import string
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

API_URL = "https://api.telegram.org/bot{token}/{method}"

HELP_TEXT = (
    "Что я умею:\n"
    "/coin - подбросить монетку\n"
    "/dice - бросить кубик\n"
    "/random 1 100 - случайное число в диапазоне\n"
    "/password 16 - надёжный пароль нужной длины\n"
    "/calc 2+2*(3+4) - калькулятор\n"
    "/time - текущее время"
)


# ---------- безопасный калькулятор ----------
OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def safe_eval(expression: str):
    """Считает выражение, разрешая только числа и + - * / ** % ().
    Использовать eval() напрямую опасно: через него можно выполнить любой код."""

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left, right = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("слишком большая степень")
            return OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](walk(node.operand))
        raise ValueError("недопустимое выражение")

    return walk(ast.parse(expression, mode="eval"))


# ---------- логика ответов (не зависит от сети) ----------
def make_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_"
    return "".join(random.SystemRandom().choice(alphabet) for _ in range(length))


def handle_message(text: str, first_name: str = "друг") -> str:
    """Принимает текст сообщения, возвращает текст ответа."""
    parts = text.strip().split()
    if not parts:
        return "Напишите /help, чтобы увидеть команды."
    command = parts[0].lower().split("@")[0]   # /start@my_bot -> /start
    args = parts[1:]

    if command == "/start":
        return f"Привет, {first_name}! Я бот-помощник.\n\n{HELP_TEXT}"
    if command == "/help":
        return HELP_TEXT
    if command == "/coin":
        return random.choice(["Орёл", "Решка"])
    if command == "/dice":
        return f"Выпало: {random.randint(1, 6)}"
    if command == "/time":
        return datetime.now().strftime("Сейчас %H:%M:%S, %d.%m.%Y")
    if command == "/random":
        try:
            low, high = (int(args[0]), int(args[1])) if len(args) >= 2 else (1, 100)
            if low > high:
                low, high = high, low
            return f"Число: {random.randint(low, high)}"
        except ValueError:
            return "Пример: /random 1 100"
    if command == "/password":
        try:
            length = int(args[0]) if args else 12
        except ValueError:
            return "Пример: /password 16"
        if not 8 <= length <= 64:
            return "Длина должна быть от 8 до 64."
        return make_password(length)
    if command == "/calc":
        expression = " ".join(args)
        if not expression:
            return "Пример: /calc 2+2*(3+4)"
        try:
            result = safe_eval(expression.replace(",", "."))
            return f"{expression} = {round(result, 10):g}"
        except ZeroDivisionError:
            return "На ноль делить нельзя."
        except (ValueError, SyntaxError, OverflowError):
            return "Не смог посчитать. Пример: /calc 2+2*(3+4)"
    return "Не понял команду. Напишите /help."


# ---------- работа с Telegram API ----------
def api_call(token: str, method: str, params: dict = None, timeout: int = 40):
    url = API_URL.format(token=token, method=method)
    data = urllib.parse.urlencode(params or {}).encode("utf-8")
    with urllib.request.urlopen(urllib.request.Request(url, data=data),
                                timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def run_bot(token: str) -> None:
    me = api_call(token, "getMe")["result"]
    print(f"Бот @{me['username']} запущен. Остановка: Ctrl+C (или Stop в Thonny).")

    offset = 0
    while True:
        try:
            updates = api_call(token, "getUpdates",
                               {"offset": offset, "timeout": 30})["result"]
            for update in updates:
                offset = update["update_id"] + 1
                message = update.get("message")
                if not message or "text" not in message:
                    continue
                name = message["from"].get("first_name", "друг")
                answer = handle_message(message["text"], name)
                api_call(token, "sendMessage",
                         {"chat_id": message["chat"]["id"], "text": answer})
                print(f"{name}: {message['text']}  ->  ответ отправлен")
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"Проблема с сетью ({error}), повтор через 5 секунд...")
            time.sleep(5)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or input("Вставьте токен бота: ").strip()
    try:
        run_bot(token)
    except urllib.error.HTTPError as error:
        if error.code in (401, 404):
            print("Telegram не принял токен. Проверьте, что скопировали его целиком.")
        else:
            print(f"Ошибка Telegram: {error}")
    except urllib.error.URLError as error:
        print(f"Нет соединения с Telegram: {error}")
    except KeyboardInterrupt:
        print("\nБот остановлен.")


if __name__ == "__main__":
    main()
