from fire import Fire

from .core import get, out


class Command:
    def output(self, format: str = "markdown", level: int = 2, language: str = "en", version: str = "5.0") -> None:
        items = get(language, version)
        out(items, format, level)


def main() -> None:
    Fire(Command)
