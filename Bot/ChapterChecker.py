from telethon import TelegramClient, events
import re
from AsyncFileManager import chapters
import os
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
channel_username = 'https://t.me/dimacrates'
SESSION_NAME = "parser_session"

TITLE_PATTERN = re.compile(r"Поднятие Уровня в Одиночку: Рагнарек - (\d+) Глава", re.IGNORECASE)
GOOGLE_DOC_PATTERN = re.compile(r"https://docs\.google\.com/document/d/[\w-]+/edit\?usp=sharing")

client = TelegramClient(SESSION_NAME, api_id, api_hash)

@client.on(events.NewMessage(chats=channel_username))
async def check_new_messages(event) -> None:
    if not event.text:
        return
    message_text = event.text.strip()
    print(message_text)
    title_match = TITLE_PATTERN.search(message_text)
    google_match = GOOGLE_DOC_PATTERN.search(message_text)

    if title_match and google_match:
        print("TITLE MATCH")
        chapter_number = int(title_match.group(1))
        print(chapter_number)
        google_link = google_match.group(0)
        print(google_link)
        comics = {"chapter": f"{chapter_number}", "link": google_link}
        await chapters.append_file(comics)