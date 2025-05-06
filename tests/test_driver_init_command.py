from argparse import Namespace
from west_commands.init_driver import DriverInitCommand
import west_commands.init_driver as module

def test_do_run_invokes_generation_and_writing(monkeypatch, tmp_path):
    # Run in a clean temp dir so nothing collides
    monkeypatch.chdir(tmp_path)

    # Prepare args with --yes to skip prompts and a RTC‐style path
    args = Namespace(
        name="drv",
        compatible="comp,any",
        bus="spi",
        path="drivers/rtc/drv",
        yes=True
    )

    cmd = DriverInitCommand()
    calls = []

    # Stub out generation and writing
    def fake_generate_files(info):
        # copy info so later mutations don't break our assertions
        calls.append(('gen', info.copy()))
        return [("f1", "c1")]

    def fake_write_files(files, path):
        calls.append(('write', files))

    monkeypatch.setattr(module, 'generate_files', fake_generate_files)
    monkeypatch.setattr(module, 'write_files', fake_write_files)

    # Execute
    ret = cmd.do_run(args, None)
    assert ret == 0

    # 1) generate_files, then 2) write_files
    assert [c[0] for c in calls] == ['gen', 'write']

    # Inspect the info dict passed to generate_files
    gen_info = calls[0][1]
    assert gen_info['name']            == 'drv'
    assert gen_info['compatible']      == 'comp,any'
    assert gen_info['bus']             == 'spi'
    assert gen_info['path']            == 'drivers/rtc/drv'
    # category is now derived from the second path segment:
    assert gen_info['category']        == 'rtc'
    # normalized fields:
    assert gen_info['uc_name']         == 'DRV'
    assert gen_info['bus_upper']       == 'SPI'
    # compatible_file is comma → underscore:
    assert gen_info['compatible_file'] == 'comp_any'

    # Finally, write_files must have been called with exactly our stubbed list
    assert calls[1][1] == [("f1", "c1")]
