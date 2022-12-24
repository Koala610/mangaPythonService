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

    def __hash__(self):
       res = 17
       res = 31 * res + self.volume
       res = 31 * res + self.chapter
       res = 31 * res + hash(self.url)
       return res

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

    def __hash__(self):
        res = 17
        res = 31 * res + hash(self.title)
        res = 31 * res + hash(self.current_chapter)
        res = 31 * res + hash(self.url)
        res = 31 * res + self.unread_chapters
        return res

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


def main():
    pass

if __name__ == "__main__":
    print(dir(RMManga))