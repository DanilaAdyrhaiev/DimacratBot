from typing import List, Dict
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboard:
    @staticmethod
    def build_keyboard(buttons: List[Dict[str, str]]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button["text"], callback_data=button["callback"]))
        return keyboard.adjust(1).as_markup()

    def get_links(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Канал Димакратия", url="https://t.me/dimacrates")],
            [InlineKeyboardButton(text="Чат Димакратия", url="https://t.me/+g4jhiBp-IhA5Zjc6")],
            [InlineKeyboardButton(text="↪️ Вернутся️", callback_data="main_menu")]
        ])
        return keyboard

    def get_chapters(self, chapter_buttons: List[Dict[str, str]], current_page: int,
                     next_chapter: bool) -> InlineKeyboardMarkup:
        prev_page = current_page - 1 if current_page > 1 else None
        next_page = current_page + 1 if next_chapter else None
        keyboard = InlineKeyboardBuilder()
        for i in range(0, min(len(chapter_buttons), 15), 3):
            row_buttons = [
                InlineKeyboardButton(
                    text=chapter_buttons[j]["chapter"],
                    callback_data=f"chapter:{chapter_buttons[j]['chapter']}"
                )
                for j in range(i, min(i + 3, len(chapter_buttons)))
            ]
            keyboard.row(*row_buttons)
        pagination_buttons = []
        if prev_page:
            pagination_buttons.append(InlineKeyboardButton(text="👈 Назад", callback_data=f"chapters:{prev_page}"))
        if next_page:
            pagination_buttons.append(InlineKeyboardButton(text="Вперёд 👉", callback_data=f"chapters:{next_page}"))
        if pagination_buttons:
            keyboard.row(*pagination_buttons)

        keyboard.row(InlineKeyboardButton(text="🔍 Поискк главы", callback_data="search_chapter"))
        keyboard.row(InlineKeyboardButton(text="↪️ Вернутся️", callback_data="main_menu"))
        return keyboard.as_markup()

    def get_chapter(self, current_chapter: int, next_chapter: bool) -> InlineKeyboardMarkup:
        pagination_buttons = []
        back_page = 1

        if current_chapter > 1:
            back_page = int(current_chapter // 15) + 1

        navigation_row = []
        if current_chapter > 0:
            navigation_row.append(InlineKeyboardButton(text="👈 Назад", callback_data=f"chapter:{current_chapter - 1}"))
        if next_chapter:
            navigation_row.append(InlineKeyboardButton(text="Вперёд 👉", callback_data=f"chapter:{current_chapter + 1}"))

        if navigation_row:
            pagination_buttons.append(navigation_row)
        pagination_buttons.append([InlineKeyboardButton(text="🔄 Обновить", callback_data=f"chapter:{current_chapter}")])
        pagination_buttons.append([InlineKeyboardButton(text="↪️ Вернутся️", callback_data="chapters:" + str(back_page))])
        pagination_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=pagination_buttons)
        return keyboard

    def get_search(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
        ])
        return keyboard


    def get_main_menu(self, buttons: List[Dict[str, str]]) -> InlineKeyboardMarkup:
        return self.build_keyboard(buttons)

    def get_anime(self) -> InlineKeyboardMarkup:
        pagination_buttons = []
        pagination_buttons.append([InlineKeyboardButton(text="1 Сезон", callback_data="season:1")])
        pagination_buttons.append([InlineKeyboardButton(text="2 Сезон", callback_data="season:2")])
        pagination_buttons.append([InlineKeyboardButton(text="↪️ Вернутся️", callback_data="main_menu")])
        return InlineKeyboardMarkup(inline_keyboard=pagination_buttons)

    def get_season(self, season: int, buttons: List[str]) -> InlineKeyboardMarkup:
        pagination_buttons = []
        for i in range(0, len(buttons), 2):
            row = []
            row.append(
                InlineKeyboardButton(text=f"Серия {buttons[i]}", callback_data=f"episode:{buttons[i]},season:{season}"))
            print(f"episode:{buttons[i]},season:{season}")
            if i + 1 < len(buttons):
                row.append(InlineKeyboardButton(text=f"Серия {buttons[i + 1]}",
                                                callback_data=f"episode:{buttons[i + 1]},season:{season}"))
                print(f"episode:{buttons[i]},season:{season}")
            pagination_buttons.append(row)
        pagination_buttons.append([InlineKeyboardButton(text="↪️ Вернутся️", callback_data="anime")])
        pagination_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])

        return InlineKeyboardMarkup(inline_keyboard=pagination_buttons)

    def get_episode(self, season: int, episode: int, buttons: Dict[str, str], next_episode: bool) -> InlineKeyboardMarkup:
        pagination_buttons = []
        navigation_row = []
        for dub, value in buttons.items():
            pagination_buttons.append([InlineKeyboardButton(text=f"Озвучка {dub}",
                                                            callback_data=f"dubs:{dub},episode:{episode},season:{season}")])
        if episode > 1:
            navigation_row.append(
                InlineKeyboardButton(text="👈 Назад", callback_data=f"episode:{episode - 1},season:{season}"))
        if next_episode:
            navigation_row.append(
                InlineKeyboardButton(text="Вперёд 👉", callback_data=f"episode:{episode + 1},season:{season}"))
        if navigation_row:
            pagination_buttons.append(navigation_row)

        pagination_buttons.append([InlineKeyboardButton(text="↪️ Вернутся️", callback_data=f"season:{season}")])
        pagination_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
        return InlineKeyboardMarkup(inline_keyboard=pagination_buttons)

    def get_dubs(self, dubs: str, episode: int, season: int, next_episode: bool) -> InlineKeyboardMarkup:
        pagination_buttons = []
        navigation_row = []
        if episode > 1:
            navigation_row.append(InlineKeyboardButton(text="👈 Назад",
                                                       callback_data=f"dubs:{dubs},episode:{episode - 1},season:{season}"))
        if next_episode:
            navigation_row.append(InlineKeyboardButton(text="Вперёд 👉",
                                                       callback_data=f"dubs:{dubs},episode:{episode + 1},season:{season}"))
        if navigation_row:
            pagination_buttons.append(navigation_row)
        pagination_buttons.append([
            InlineKeyboardButton(text="↪️ Вернутся️", callback_data=f"back_to_season,episode:{episode},season:{season}")
        ])
        pagination_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main_from_video")])
        return InlineKeyboardMarkup(inline_keyboard=pagination_buttons)
