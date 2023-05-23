from src.core_entity.protocol.manga_protocol import Manga
from typing import Tuple
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from src.core_logger import logger

def create_bookmark_response(bookmark: Manga) -> Tuple[str, InlineKeyboardMarkup]:
    text = str(bookmark)
    open_page_btn = InlineKeyboardButton("Открыть страницу", url=f"https://readmanga.live/{bookmark.url}")
    current_chapter_url = bookmark.current_chapter.url or "https://readmanga.live"
    resume_btn = InlineKeyboardButton("Продолжить чтение", url=f"{current_chapter_url}" )
    inline_manga_menu = InlineKeyboardMarkup().add(open_page_btn)
    if bookmark.current_chapter.volume != -1:
        inline_manga_menu.add(resume_btn)
    return text, inline_manga_menu

def create_unread_response(bookmark: Manga) -> Tuple[str, InlineKeyboardMarkup]:
    text = str(bookmark)
    text += f"Кол-во непрочитанных: {bookmark.unread_chapters}"
    open_page_btn = InlineKeyboardButton("Открыть страницу", url=f"https://readmanga.live/{bookmark.url}")
    current_chapter_url = bookmark.current_chapter.url or "https://readmanga.live"
    resume_btn = InlineKeyboardButton("Продолжить чтение", url=f"{current_chapter_url}" )
    inline_manga_menu = InlineKeyboardMarkup().add(open_page_btn)
    inline_manga_menu.add(resume_btn)
    return text, inline_manga_menu