import builtins
import pytest
from west_commands.init_driver import ask_value
from argparse import Namespace


def test_flag_with_yes_returns_value():
    args = Namespace(name="foo", yes=True)
    assert ask_value(args, 'name', 'Driver name', 'default') == "foo"


def test_prompt_when_no_flag(monkeypatch):
    args = Namespace(name=None, yes=False)
    monkeypatch.setattr(builtins, 'input', lambda prompt: "bar")
    assert ask_value(args, 'name', 'Driver name', 'default') == "bar"


def test_default_on_empty_input(monkeypatch):
    args = Namespace(name=None, yes=False)
    monkeypatch.setattr(builtins, 'input', lambda prompt: "")
    assert ask_value(args, 'name', 'Driver name', 'default') == "default"
