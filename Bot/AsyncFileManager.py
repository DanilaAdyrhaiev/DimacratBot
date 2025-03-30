import asyncio
import json

class AsyncFileManager:
    def __init__(self, filename):
        self.filename = filename
        self.file_lock = asyncio.Lock()

    async def read_file(self):
        async with self.file_lock:
            with open(self.filename, "r", encoding="utf-8") as file:
                content = await asyncio.to_thread(file.read)
                return json.loads(content)

    async def write_file(self, data):
        async with self.file_lock:
            await asyncio.to_thread(self._sync_write_file, data)

    def _sync_write_file(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    async def append_file(self, new_entry):
        data = await self.read_file()
        data.append(new_entry)
        await self.write_file(data)


pages = AsyncFileManager("data/pages.json")
chapters = AsyncFileManager("data/chapters.json")
anime = AsyncFileManager("data/anime.json")
users = AsyncFileManager("data/users.json")