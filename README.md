# Трекер цен с Claude


[![hexlet-check](https://github.com/iakunin/vibecoding-claudecode-project-388/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/iakunin/vibecoding-claudecode-project-388/actions)

Соберите на Claude-скиллах трекер цен: он сам следит за товарами и присылает в Telegram только значимые изменения.

Учебный проект Хекслета: https://ru.hexlet.io/programs/vibecoding-claudecode


## Стек

- **Claude Code + Skills** — вся логика трекера живёт в скиллах:
  - [`extract-price`](.claude/skills/extract-price/SKILL.md) — один URL → `{regular_price, sale_price, has_credit}`;
  - [`tracker`](.claude/skills/tracker/SKILL.md) — обход списка, таблица прогона, сравнение с прошлым, сохранение и отправка.
- **Субагент на Haiku** — [`telegram-summary`](.claude/agents/telegram-summary.md) оформляет текст сводки из готового списка изменений.
- **[`KNOWLEDGE.md`](KNOWLEDGE.md)** — правила значимости изменений: пороги, скидки, рассрочка.
- **Python 3 (стандартная библиотека)** — [`send.py`](send.py), отправка сообщения через Telegram Bot API.
- **GitHub Contents API** — история прогонов в отдельном приватном репозитории `tracker-data`, по файлу `YYYY-MM-DD.json` на день.

## Установка

Нужны [Claude Code](https://claude.com/claude-code), Python 3, `curl` и авторизованный `gh` (`gh auth login`) — токен для записи в `tracker-data` берётся из `gh auth token`.

```bash
git clone https://github.com/iakunin/vibecoding-claudecode-project-388.git
cd vibecoding-claudecode-project-388
```

Создайте `.env` в корне (он в `.gitignore`):

```bash
TELEGRAM_BOT_TOKEN=...   # токен бота от @BotFather
TELEGRAM_CHAT_ID=...     # id чата, куда слать сводки
```

Проверить доставку:

```bash
python3 send.py "Проверка связи"
```

## Использование

Запустите `claude` в корне репозитория и напишите в чате:

```
запусти трекер
```

Подойдёт и «проверь цены» или «что изменилось по ценам». Дальше скилл `tracker`:

1. По очереди, с паузой, вызывает `extract-price` для каждого товара из списка.
2. Собирает таблицу прогона: `regular_price`, `sale_price`, `has_credit` по каждому товару.
3. Читает из `tracker-data` предыдущий прогон и оставляет только значимые изменения по правилам из `KNOWLEDGE.md`.
4. Сохраняет свежий прогон в `tracker-data` как `YYYY-MM-DD.json` одним коммитом.
5. Отправляет сводку в Telegram — одно сообщение на прогон:

```
📉 Изменения цен 2026-09-20

🔻 ADAM A4V (чёрный): 49 500 → 48 600 ₽ (−1.8%)
💳 ADAM A77H: появилась рассрочка
```

Если значимых изменений нет, придёт `✅ Цены на месте, значимых изменений нет`. На первом прогоне сравнивать не с чем, поэтому придёт снимок всех цен. Полную таблицу прогона можно попросить явно: «запусти трекер и покажи всю таблицу».

Цену одного товара можно узнать и без трекера: «сколько стоит https://united-music.ru/ru/adam-a4v.html».

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.


---

## Какие товары я отслеживаю

Мониторные колонки. В частности:
- https://united-music.ru/ru/adam-a4v.html
- https://united-music.ru/ru/adam-a4v-white.html
- https://united-music.ru/ru/adam-a7v.html
- https://united-music.ru/ru/adam-a7v-white.html
- https://united-music.ru/ru/adam-a77h.html
- https://united-music.ru/ru/adam-a8h-b-side.html
- https://united-music.ru/ru/adam-a8h-a-side.html


## Зачем я отслеживаю цены

Для того, чтобы подгадать для себя наиболее выгодный момент покупки