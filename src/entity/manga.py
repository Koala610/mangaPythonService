import hashlib
from dataclasses import dataclass

@dataclass
class RMChapter:
    volume: int = 0
    chapter: int = 0
    url: str = ""

    def __str__(self):
        if self.volume == -1:
            return "Недоступно"
        return f"{self.volume} том, {self.chapter} глава"

    def get_hash(self):
        hash_object = hashlib.md5()
        hash_object.update(str(self).encode())
        return int(hash_object.hexdigest(), 16)

@dataclass
class RMManga:
    title: str
    current_chapter: RMChapter
    url: str
    unread_chapters: int = 0

    def __str__(self):
        result = "Название: " + self.title + "\n"
        result += "Текущая глава: " + str(self.current_chapter) + "\n"
        # result += "Кол-во непрочитанных глав: " + str(self.unread_chapters)
        return result

    def get_hash(self):
        hash_object = hashlib.md5()
        hash_object.update(str(self).encode())
        return int(hash_object.hexdigest(), 16)

    @classmethod
    def from_json(cls, data: dict) -> object:
       element =  data.get("element")
       title =element.get("name") 
       volume = data.get("vol") or -1
       num = data.get("num") or -1
       resume = data.get("resume")
       chapter_url = resume.get("url") if resume is not None else ""
       chapter = RMChapter(int(volume), int(num/10), url=chapter_url)
       manga_url = element.get("elementId").get("linkName")
       new_chapters = data.get("newChapters")
       result = cls(title=title, current_chapter=chapter, url=manga_url, unread_chapters=new_chapters)
       return result

    @classmethod
    def hash_from_list(cls, l: list):
        res = 17
        for i in l:
            res = 31 * res + i.get_hash()
        return res


def main():
    h = hashlib.sha256()
    a = [RMManga("13", RMChapter(1, 1, "13"), "123", 123)]
    print(RMManga.hash_from_list(a))
if __name__ == "__main__":
    main()