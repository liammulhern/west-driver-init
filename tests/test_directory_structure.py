
import os
from pathlib import Path
import pytest
from argparse import Namespace

# adjust import to wherever your DriverInitCommand lives:
from west_commands.init_driver import DriverInitCommand


def test_directory_structure(tmp_path, monkeypatch):
    # Run in a clean temp directory
    monkeypatch.chdir(tmp_path)

    # Prepare args for a driver named "mcp7940mt" under path "drivers/rtc/mcp7940mt"
    args = Namespace(
        name="mcp7940mt",
        compatible="microchip,mcp7940",
        bus="i2c",
        path="drivers/rtc/mcp7940mt",
        yes=True
    )

    cmd = DriverInitCommand()
    # ensure color_ui override if you applied it
    # cmd.color_ui = False

    # Execute the command
    ret = cmd.do_run(args, None)
    assert ret == 0

    # Base folder for the new driver
    base = tmp_path / "drivers" / "rtc" / "mcp7940mt"

    # Define the files we expect
    expected = [
        # public header
        base / "include" / "drivers" / "rtc" / "mcp7940mt.h",
        # C source
        base / "src" / "mcp7940mt.c",
        # Kconfig and CMakeLists.txt
        base / "Kconfig",
        base / "CMakeLists.txt",
        # DTS binding: uses the compatible string, with comma→underscore
        base / "dts" / "bindings" / "rtc" / "microchip_mcp7940.yaml",
    ]

    # Assert each exists and is non-empty
    for p in expected:
        assert p.exists(), f"Expected {p} to exist"
        assert p.is_file(), f"{p} should be a file"
        # Optionally, check it has at least 1 byte
        assert p.stat().st_size > 0, f"{p} should not be empty"
