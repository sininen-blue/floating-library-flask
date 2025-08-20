from .parser import Parser
from .pageParsers import qq


def parse(url: str) -> dict[str, str | list[str]]:
    # look at url
    # figure out which parser it needs
    # login if required

    # TODO: turn paeg parsers into PageParsers class
    # and use composition instead

    parser: Parser = qq.QqParser()
    results: dict[str, str | list[str]]
    try:
        results = parser.parse(url)
    except Exception as e:
        results["errors"].append(f"Parse error: {e}")

    return results
