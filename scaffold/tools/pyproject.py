from pathlib import Path

import tomli
import tomli_w


class PyProject:
    def __init__(self, project_name: str) -> None:
        self.path = Path(project_name, "pyproject.toml")
        with self.path.open("rb") as fr:
            self.data = tomli.load(fr)

    def add(self, key, value) -> None:
        self.data["tool"][key] = value

    def save(self):
        # todo: how to sort data
        with self.path.open("wb") as fw:
            tomli_w.dump(self.data, fw)
