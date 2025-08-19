from requests import Session, Response, get
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv
import os
from requests import Session

load_dotenv()


class Parser:
    def __init__(
        self,
        login_page: str | None = None,
        login_post: str | None = None,
        csrf_key: str | None = None
    ) -> None:
        self.login_page: str = login_page
        self.login_post: str = login_post
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

        response: Response = session.post(
            self.login_post,
            data=payload, headers=headers, timeout=10
        )
        response.raise_for_status()

        # TODO: confirm if logged in
        # figure out where it redirects
        # check if it redirects to that site

        print("logged in successfully")

        self.session = session

    def pull(self, url: str) -> BeautifulSoup:
        response: Response
        if self.session is not None:
            response: Response = self.session.get(url, timeout=10)
        else:
            response: Response = get(url, timeout=10)

        response.raise_for_status()

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        return soup

    def parse(self, url: str) -> dict[str, str | list[str]]:
        info: dict[str, str | list[str]] = {}
        return info

    def add_to_info(
        self, info: dict[str, str | list[str]],
        key: str, chunk: Tag | None
    ) -> None:
        if chunk is not None:
            info[key] = chunk.text.strip()
        else:
            info["errors"].append(f"Could not find {key}")
