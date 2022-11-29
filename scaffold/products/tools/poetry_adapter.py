import subprocess
import sys


class Poetry:
    cwd: str = None

    def invoke(self, command: str, *options: list[str]) -> None:
        try:
            subprocess.run(["poetry", command, *options], check=True, cwd=self.cwd)
        except subprocess.CalledProcessError:
            sys.exit(1)

    def new(self, project_name: str) -> None:
        self.invoke("new", project_name)
        self.cwd = project_name

    def add(self, package_name: str, dev: bool = False) -> None:
        assert self.cwd is not None, "Only available after calling `new()`"
        if dev:
            self.invoke("add", "--group", "dev", package_name)
        else:
            self.invoke("add", package_name)

    def run(self, *options: list[str]) -> None:
        assert self.cwd is not None, "Only available after calling `new()`"
        self.invoke("run", *options)
