from pathlib import Path

import toml  # type: ignore


class PyProject:
    def __init__(self, project_name: str) -> None:
        self.path = Path(project_name, "pyproject.toml")
        with self.path.open("r", encoding="utf8") as fr:
            self.data = toml.load(fr)

    def add(self, key, value) -> None:
        self.data["tool"][key] = value

    def save(self):
        # todo: how to sort data
        with self.path.open("w", encoding="utf8") as fw:
            toml.dump(self.data, fw)
