import requests
from git import Repo


class Git:
    repo: Repo = None

    def init(self, project_name: str, gitignore: bool = False) -> None:
        self.repo = Repo.init(project_name)
        if gitignore:
            url = "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore"
            response = requests.get(url, timeout=10)
            with open(f"{project_name}/.gitignore", "w", encoding="utf-8") as fw:
                fw.write("# Github gitignore template: Python\n")
                fw.write(f"# {url}\n")
                fw.write(response.text)

    def add(self) -> None:
        self.repo.git.add(all=True)

    def commit(self, message: str) -> None:
        self.repo.git.commit("-m", message)

    def rename_branch(self, branch_name: str = "main") -> None:
        self.repo.git.branch("-m", branch_name)
