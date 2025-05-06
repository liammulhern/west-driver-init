import pytest
from west_commands.init_driver import render_template


def test_render_template_success():
    template = "Hello {name}"
    info = {"name": "World"}
    assert render_template(template, info) == "Hello World"


def test_render_template_missing_key():
    template = "Missing {key}"
    with pytest.raises(KeyError):
        render_template(template, {})
