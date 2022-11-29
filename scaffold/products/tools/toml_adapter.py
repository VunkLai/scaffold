from pathlib import Path

import tomli
import tomli_w


class TomlConfiguration(dict):
    path: Path = None

    def initialize(self, project_name: str, filename: str = "pyproject.toml") -> None:
        self.path = Path(project_name, filename)
        assert self.path.exists(), "Only available after calling `poetry init`"
        self.refresh()

    def refresh(self) -> None:
        with self.path.open("rb") as fr:
            data = tomli.load(fr)
            for key, value in data.items():
                setattr(key, value)

    def save(self) -> None:
        with self.path.open("wb") as fw:
            tomli_w.dump(self, fw)
