from argparse import Namespace
from west_commands.init_driver import DriverInitCommand
import west_commands.init_driver as module


def test_do_run_invokes_generation_and_writing(monkeypatch):
    # Prepare args with --yes to skip prompts
    args = Namespace(name="drv",
                     compatible="comp",
                     bus="i2c",
                     path="drivers/i2c/drv",
                     yes=True)
    cmd = DriverInitCommand()
    calls = []
    # Stub out generation and writing
    monkeypatch.setattr(module, 'generate_files', lambda info: calls.append(('gen', info)) or [("f1","c1")])
    monkeypatch.setattr(module, 'write_files', lambda files: calls.append(('write', files)))

    ret = cmd.do_run(args, None)
    assert ret == 0
    assert [c[0] for c in calls] == ['gen', 'write']
    assert calls[1][1] == [("f1","c1")]
