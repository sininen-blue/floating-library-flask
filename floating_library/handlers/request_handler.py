from flask import Request


class RequestHandler():
    def __init__(self, request: Request):
        self._request = request

    def get(self, key: str, optional: bool = False) -> str:
        item: str | None = self._request.form.get(key, type=str)

        if item is None and not optional:
            return f"{key} is a required input"

        return item
