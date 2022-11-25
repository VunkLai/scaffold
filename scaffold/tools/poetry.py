import subprocess
import sys


class Poetry:
    def __init__(self, project_name: str) -> None:
        self.project_name = project_name

    def new(self) -> None:
        try:
            subprocess.run(["poetry", "new", self.project_name], check=True)
        except subprocess.CalledProcessError:
            sys.exit(1)

    def add(self, dependencies: list[str], dev: bool = False) -> None:
        try:
            cmd = ["poetry", "add"]
            if dev:
                cmd.extend(["--group", "dev"])
            cmd.extend(dependencies)
            subprocess.run(cmd, cwd=self.project_name, check=False)
        except subprocess.CalledProcessError:
            sys.exit(1)
