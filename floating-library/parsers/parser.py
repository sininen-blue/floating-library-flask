from requests import Session, Response, get
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
from urllib.parse import urljoin
import os

load_dotenv()


class Parser:
    REQUIRED_KEYS: list[str] = [
        "title_tag",
        "title_class",
        "author_tag",
        "author_class",
        "chapter_count_tag",
        "chapter_count_class",
    ]

    def __init__(
        self,
        base_page: str,
        login_page: str,
        csrf_key: str,
        queries: dict[str, str]
    ) -> None:
        missing = [key for key in self.REQUIRED_KEYS if key not in queries]
        if missing:
            raise ValueError(
                f"Missing required parser keys: {', '.join(missing)}"
            )

        self.queries = queries
        self.base_page: str = base_page
        self.login_page: str = login_page
        self.csrf_key: str = csrf_key
        self.session: Session | None = None

    def login(self) -> None:
        session: Session = Session()

        # get login page
        login_page_response: Response = session.get(self.login_page)
        soup: BeautifulSoup = BeautifulSoup(
            login_page_response.text, "html.parser"
        )

        # get csrf token
        csrf_token_input: Tag = soup.find("input", {"name": self.csrf_key})
        if not csrf_token_input:
            raise Exception("CSRF token not found on login page")
        csrf_token: str = csrf_token_input.get("value")

        # login
        payload: dict[str, str] = {
            "login": os.getenv("DEFAULT_USER"),
            "password": os.getenv("DEFAULT_PASSWORD"),
            self.csrf_key: csrf_token
        }
        headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}

        try:
            response: Response = session.post(
                urljoin(self.login_page, "login"),
                data=payload, headers=headers, timeout=10
            )
        except Exception as e:
            raise Exception(f"Failed to login: {e}")
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code} error")

        self.session = session

    def parse(self, url: str) -> dict[str, str | list[str]]:
        info: dict[str, str | list[str]] = {}
        info["errors"]: list = []

        try:
            response: Response = get(url, timeout=10)
        except Exception as e:
            info["errors"].append(f"Request failed: {e}")
            return info
        if response.status_code != 200:
            info["errors"].append(f"HTTP {response.status_code} error")
            return info

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        element_list: list[str] = ["title", "author", "chapter_count"]
        for element in element_list:
            tag = self.queries.get(f"{element}_tag")
            class_name = self.queries.get(f"{element}_class")

            chunk: Tag | None = soup.find(tag, class_=class_name)

            if chunk is not None:
                info[element] = chunk.text
            else:
                info["error"].append(f"Could not find {element}")

        return info
