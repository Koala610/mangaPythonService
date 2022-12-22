from src.entity.protocol.manga_protocol import Manga
from typing import Tuple
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

def create_bookmark_response(bookmark: Manga) -> Tuple[str, InlineKeyboardMarkup]:
    text = str(bookmark)
    open_page_btn = InlineKeyboardButton("Открыть страницу", url=f"https://readmanga.live/{bookmark.url}")
    current_chapter_url = bookmark.current_chapter.url or "https://readmanga.live"
    resume_btn = InlineKeyboardButton("Продолжить чтение", url=f"{current_chapter_url}" )
    inline_manga_menu = InlineKeyboardMarkup().add(open_page_btn, resume_btn)
    return text, inline_manga_menu