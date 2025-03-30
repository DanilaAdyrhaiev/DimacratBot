from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaVideo
from keyboard import Keyboard
import json
import re
from AsyncFileManager import pages, chapters, anime, users
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()
keyboard = Keyboard()

class ChapterSearch(StatesGroup):
    waiting_for_chapter_number = State()

@router.message(CommandStart())
async def start_main_menu_page(message: Message):
    try:
        users_data = await users.read_file()
        if not isinstance(users_data, list):
            users_data = []
    except json.JSONDecodeError:
        users_data = []
    user_id = str(message.from_user.id)
    full_name = message.from_user.full_name
    user_exists = any(user["id"] == user_id for user in users_data)
    if not user_exists:
        users_data.append({"id": user_id, "name": full_name})
        await users.write_file(users_data)
    data = await pages.read_file()
    main_menu: dict = data["main_menu"]
    await message.answer(main_menu["text"], reply_markup=keyboard.get_main_menu(main_menu["buttons"]))

@router.callback_query(F.data == "main_menu")
async def callback_main_menu_page(callback: CallbackQuery):
    data = await pages.read_file()
    main_menu: dict = data["main_menu"]
    await callback.message.edit_text(main_menu["text"], reply_markup=keyboard.get_main_menu(main_menu["buttons"]))

@router.callback_query(F.data.startswith("chapters"))
async def chapters_page(callback: CallbackQuery):
    match = re.match(r"^chapters:(\d+)$", callback.data)
    current_page = int(match.group(1)) if match else 1
    all_data = await chapters.read_file()
    start = (current_page - 1) * 15
    end = current_page * 15

    data = all_data[start:end]

    await callback.message.edit_text(
        text=f"Главы ранобэ с {start} по {end}",
        reply_markup=keyboard.get_chapters(
            data,
            current_page,
            end < len(all_data),
        ),
    )

@router.callback_query(F.data == "search_chapter")
async def start_chapter_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Введите номер главы, которую хотите найти:",
        reply_markup=keyboard.get_search()
    )
    await state.set_state(ChapterSearch.waiting_for_chapter_number)
    await callback.answer()

@router.message(ChapterSearch.waiting_for_chapter_number, F.data == "cancel")
async def cancel_search(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await start_chapter_search(callback)

@router.message(ChapterSearch.waiting_for_chapter_number)
async def process_chapter_search(message: Message, state: FSMContext):
    await state.clear()
    chapter_number = message.text.strip()
    current_page = 1
    all_data = await chapters.read_file()

    if not chapter_number.isdigit():
        start = (current_page - 1) * 15
        end = current_page * 15
        data = all_data[start:end]
        bot = message.bot
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id, message.message_id - 1])
        await message.answer(text="Некоректно введена глава",
                             reply_markup=keyboard.get_chapters(
                                 data,
                                 current_page,
                                 end < len(all_data),
                             ))
        return
    chapter_number = int(chapter_number)
    if 0 <= chapter_number < len(all_data):
        chapter: dict = all_data[chapter_number]
        next_chapter = chapter_number + 1 < len(all_data)
        bot = message.bot
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id, message.message_id - 1])
        await message.answer(text=f"Глава {chapter_number}\n{chapter.get('link')}", reply_markup=keyboard.get_chapter(chapter_number, next_chapter))
    else:
        start = (current_page - 1) * 15
        end = current_page * 15
        data = all_data[start:end]
        bot = message.bot
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id, message.message_id - 1])
        await message.answer(text=f"Глава {chapter_number} не найдена.",
                             reply_markup=keyboard.get_chapters(
                                 data,
                                 current_page,
                                 end < len(all_data),
                             ))

@router.callback_query(F.data.startswith("chapter:"))
async def chapter_page(callback: CallbackQuery):
    match = re.match(r"^chapter:(\d+)$", callback.data)
    numb_chapter = int(match.group(1)) if match else 0
    data = await chapters.read_file()
    chapter: dict = data[numb_chapter]
    next_chapter = numb_chapter + 1 < len(data)
    await callback.message.edit_text(text=f"Глава {numb_chapter}\n{chapter.get('link')}", reply_markup=keyboard.get_chapter(numb_chapter, next_chapter))


@router.callback_query(F.data == "anime")
async def anime_page(callback: CallbackQuery):
    data = await pages.read_file()
    anime: dict = data["anime"]
    await callback.message.edit_text(text=anime["text"], reply_markup=keyboard.get_anime())

@router.callback_query(F.data == "links")
async def link_page(callback: CallbackQuery):
    await callback.message.edit_text(text="Есть вопросы и пожелания?\nНапишите на почту:\nfahsh2701@gmail.com", reply_markup=keyboard.get_links())


@router.callback_query(lambda c: c.data.startswith("season:"))
async def season_page(callback: CallbackQuery):
    match = re.match(r"^season:(\d+)$", callback.data)
    season = int(match.group(1)) if match else 1
    data = await anime.read_file()
    data = data["seasons"]
    season_data = data.get(f"{season}", {})
    episodes = list(season_data["episodes"].keys())
    await callback.message.edit_text(
        text=f"Сезон {season}",
        reply_markup=keyboard.get_season(season, episodes)
    )

@router.callback_query(F.data.startswith("episode:"))
async def episode_page(callback: CallbackQuery):
    match = re.match(r"^episode:(\d+),season:(\d+)$", callback.data)
    episode = int(match.group(1)) if match else 1
    season = int(match.group(2)) if match else 1
    data = await anime.read_file()
    season_data = data.get('seasons', {}).get(str(season), {}).get('episodes', {})
    episode_data = season_data.get(str(episode), {})
    next_episode = str(episode + 1) in season_data

    if episode_data:
        await callback.message.edit_text(
            text=f"Сезон {season}, Эпизод {episode}",
            reply_markup=keyboard.get_episode(season, episode, episode_data, next_episode)
        )
    else:
        await callback.answer("Эпизод не найден")

@router.callback_query(F.data.startswith("dubs:"))
async def dubs_page(callback: CallbackQuery):
    match = re.match(r"^dubs:(.+),episode:(\d+),season:(\d+)$", callback.data)
    dubs = match.group(1) if match else None
    episode = int(match.group(2)) if match else 1
    season = int(match.group(3)) if match else 1
    data = await anime.read_file()
    season_data = data.get('seasons', {}).get(str(season), {}).get('episodes', {})

    if str(episode) in season_data and dubs in season_data[str(episode)]:
        video_id = season_data[str(episode)][dubs]  # Получаем ID видео
        next_episode = str(episode + 1) in season_data

        media = InputMediaVideo(
            media=video_id,
            caption=f"Сезон {season}, Эпизод {episode}, Озвучка {dubs}"
        )

        await callback.message.edit_media(
            media=media,
            reply_markup=keyboard.get_dubs(dubs, episode, season, next_episode)
        )
    else:
        await callback.answer("Эпизод не найден или озвучка отсутствует")

@router.callback_query(F.data.startswith("back_to_season"))
async def back_to_episode_from_video(callback: CallbackQuery):
    try:
        match = re.match(r"back_to_season,episode:(\d+),season:(\d+)",
                         callback.data)
        episode = int(match.group(1)) if match else 1
        season = int(match.group(2)) if match else 1
        print(season, episode)
        data = await anime.read_file()
        season_data = data['seasons'].get(str(season), {'episodes': {}})
        episodes = season_data.get('episodes', {})
        episode_data = episodes.get(str(episode), {})
        next_episode = str(episode + 1) in episodes
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=f"Сезон {season}, Эпизод {episode}",
            reply_markup=keyboard.get_episode(season, episode, episode_data, next_episode)
        )

        await callback.message.delete()

    except Exception as e:
        print(f"Ошибка в back_to_season_from_video: {e}")
        await callback.answer(f"Произошла ошибка: {str(e)}")


@router.callback_query(lambda c: c.data == "back_to_main_from_video")
async def back_to_main_from_video(callback: CallbackQuery):
    await callback.message.delete()
    data = await pages.read_file()
    main_menu: dict = data["main_menu"]

    await callback.message.answer(
        text=main_menu["text"],
        reply_markup=keyboard.get_main_menu(main_menu["buttons"])
    )
