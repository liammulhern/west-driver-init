from west_commands.init_driver import write_files


def test_write_and_create_dirs(tmp_path, monkeypatch):
    # Change cwd to tmp_path
    monkeypatch.chdir(tmp_path)
    files = [
        ("dir_a/b.txt", "hello"),
        ("c.txt", "world")
    ]
    write_files(files)
    assert (tmp_path / "dir_a" / "b.txt").read_text() == "hello"
    assert (tmp_path / "c.txt").read_text() == "world"
