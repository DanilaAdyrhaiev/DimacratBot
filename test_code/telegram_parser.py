from telethon.sync import TelegramClient
import re
import asyncio
import json

# Укажите свои API_ID и API_HASH
api_id = ""
api_hash = ""
channel_username = 'https://t.me/dimacrates'
SESSION_NAME = "parser_session"

TITLE_PATTERN = re.compile(r"Поднятие Уровня в Одиночку: Рагнар[её]к.*?(\d+)\s*Глава", re.IGNORECASE)
GOOGLE_DOC_PATTERN = re.compile(r"https://docs\.google\.com/document/d/[\w-]+/edit\?usp=sharing")


async def main():
    async with TelegramClient(SESSION_NAME, api_id, api_hash) as client:
        # Получаем все сообщения с расширенным лимитом
        messages = await client.get_messages(channel_username, limit=None)
        found_chapters = {}

        for message in messages:
            if not message.text:
                continue

            # Улучшенный поиск главы и ссылки
            title_match = TITLE_PATTERN.search(message.text)
            google_match = GOOGLE_DOC_PATTERN.search(message.text)

            if title_match and google_match:
                chapter_number = int(title_match.group(1))
                google_link = google_match.group(0)

                # Сохраняем только главы в диапазоне 330-312
                if 312 <= chapter_number <= 330:
                    found_chapters[chapter_number] = google_link

        # Подготовка JSON-выхода с сортировкой от меньшего к большему
        json_output = []
        for chapter, link in sorted(found_chapters.items()):
            json_output.append({
                "chapter": str(chapter),
                "link": link
            })

        # Вывод JSON
        print(json.dumps(json_output, indent=4, ensure_ascii=False))

        # Пропущенные главы (для информативности)
        missing_chapters = [chapter for chapter in range(330, 311, -1)
                            if chapter not in found_chapters]
        if missing_chapters:
            print(f"\nПропущены главы: {missing_chapters}")


asyncio.run(main())