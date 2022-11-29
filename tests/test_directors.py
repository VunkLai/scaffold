from scaffold.directors import Director, Scaffold


class FakeBuilder:
    pass


FAKE_PROJECT_NAME = "directors-test-project"


def test_director_and_builder():
    director = Director()
    director.builder = FakeBuilder()
    assert isinstance(director.builder, FakeBuilder)


def test_scaffold_director(mocker):
    scaffold = Scaffold()
    assert isinstance(scaffold, Director)

    scaffold.builder = FakeBuilder()
    assert hasattr(scaffold, "create_python_project")
    assert callable(scaffold.create_python_project)

    spy = mocker.spy(scaffold, "create_python_project")
    scaffold.create_python_project(FAKE_PROJECT_NAME)
    assert spy.called

    assert hasattr(scaffold, "create_vscode_project")
    scaffold.create_vscode_project()
    assert spy.called
