from west_commands.init_driver import generate_files


def test_generate_single_file():
    templates = {"file_{n}.txt": "Num {n}"}
    info = {"n": "1"}
    assert generate_files(info, templates) == [("file_1.txt", "Num 1")]


def test_generate_multiple_files():
    templates = {
        "{n}.md": "# {n}",
        "{n}.txt": "Val {v}"
    }
    info = {"n": "x", "v": "y"}
    result = dict(generate_files(info, templates))
    assert result["x.md"] == "# x"
    assert result["x.txt"] == "Val y"
