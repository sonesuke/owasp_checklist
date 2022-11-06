from fire import Fire

from .core import get, out


class Command:
    def github(self, level: int, api_key: str, language: str, version: str) -> None:
        pass

    def output(self, level: int = 2, format: str = "markdown", language: str = "en", version: str = "4.0") -> None:
        items = get(language, version)
        out(items, format, level)


def main() -> None:
    Fire(Command)
