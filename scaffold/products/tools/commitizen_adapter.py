from commitizen.commands import Init
from commitizen.config import TomlConfig

INITIAL_CONFIG = {
    "name": "cz_conventional_commits",
    "version": "0.0.1",
    "tag_format": "$version",
}


class Commitizen(Init):
    def __init__(self) -> None:
        self.config = TomlConfig(data="", path="pyproject.toml")
        self.config.init_empty_config_content()
        super().__init__(self.config)

    def initialize(self, pre_commit: bool = False) -> None:
        self._update_config_file(INITIAL_CONFIG)
        if pre_commit:
            self._install_pre_commit_hook()
