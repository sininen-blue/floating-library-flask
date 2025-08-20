from floating_library.parsers.parser import Parser
from bs4 import BeautifulSoup, Tag


class QqParser(Parser):
    def __init__(
        self,
        login_page: str = 'https://forum.questionablequesting.com/login/',
        login_post: str = 'https://forum.questionablequesting.com/login/login',
        csrf_key: str = '_xfToken',
    ) -> None:
        super().__init__(login_page, login_post, csrf_key)

    def parse(self, url) -> dict[str, str | list[str]]:
        info: dict[str, str | list[str]] = {}

        self.login()
        soup: BeautifulSoup = self.pull(url)

        title_chunk: Tag | None = soup.find("h1", class_="p-title-value")
        self.add_to_info(info, "title", title_chunk)

        author_chunk: Tag | None = soup.find(
            "a", class_="username u-concealed"
        )
        self.add_to_info(info, "author", author_chunk)

        chapter_block_chunk: Tag | None = soup.find(
            "dl", class_="pairs pairs--rows fauxBlockLink"
        )
        if chapter_block_chunk is not None:
            chapter_count_chunk: Tag = chapter_block_chunk.find("dd")
            self.add_to_info(info, "chapter_count", chapter_count_chunk)
        else:
            info["errors"].append("Could not find chapter count block")

        return info
