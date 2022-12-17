import bs4
import src.logger as logger

from typing import Tuple
from dataclasses import dataclass


@dataclass
class RmParsedManga:
    title: str
    description: str


class ReadmangaParser:
    def parse_manga_page(self, html: str) -> RmParsedManga:
        pass

    def parse_bookmarks(self, html: str) -> Tuple[RmParsedManga]:
        pass

    def parse_auth_page(self, html: str) -> dict:
        """
        url : form.action  \/

        response:
            targetUri : form.input.value
            username: %custom%
            password: %custom%
            remember_me: "true"
            _remember_me_yes: ""
            remember_me_tes: "on"
        required headers:
            Content-Type: application/x-www-form-urlencoded
            DNT: 1
        response string format: 
            targetUri={targer_uri}&username={username}&password={password}&remember_me=true&_remember_me_yes=&remember_me_yes=on 

        """
        soup = bs4.BeautifulSoup(html, features="html.parser")
        form = soup.find("form")
        url = form.attrs["action"]
        targer_uri = form.find("input", {"name": "targetUri"})["value"]
        logger.logger.info("Auth page successfully parsed...")
        return {
            "url": url,
            "target_uri": targer_uri
        }
