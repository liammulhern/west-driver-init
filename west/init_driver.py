import os
import argparse
from west.commands import WestCommand
from west import log

TEMPLATE_FILES = {
    "include/drivers/{path}/__driver__.h": """\
/*
 * @file
 * @brief Skeleton header for {name} driver
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_{uc_name}_H_
#define ZEPHYR_INCLUDE_DRIVERS_{uc_name}_H_

#include <device.h>
#include <zephyr/types.h>

#ifdef __cplusplus
extern "C" {{
#endif

/**
 * @brief Initialize the {name} device.
 *
 * @param dev Device struct
 * @return 0 on success, negative errno on failure
 */
int {name}_init(const struct device *dev);

#ifdef __cplusplus
}}
#endif

#endif /* ZEPHYR_INCLUDE_DRIVERS_{uc_name}_H_ */
""",
    "src/{path}/__driver__.c": """\
/*
 * @file
 * @brief Skeleton implementation for {name} driver
 */

#include <device.h>
#include <drivers/{category}/{name}.h>
#include <init.h>

static int {name}_init_fn(const struct device *dev) {{
    ARG_UNUSED(dev);
    /* TODO: your init code here */
    return 0;
}}

DEVICE_INIT({name}, "{name}", {name}_init_fn,
            NULL, NULL, POST_KERNEL,
            CONFIG_KERNEL_INIT_PRIORITY_DEFAULT);
""",
    "Kconfig": """\
menu "Custom Driver Options"

config {uc_name}
    bool "Enable {name} driver"
    default n
    help
      Enable the {name} driver.  Requires CONFIG_{bus_upper}_IFACE=y.
endmenu
""",
    "CMakeLists.txt": """\
zephyr_library()
zephyr_library_sources_ifdef(CONFIG_{uc_name} src/{path}/{name}.c)
zephyr_library_include_directories(include)
""",
    "dts/bindings/{category}/{name}.yaml": """\
/*
 * Device tree binding for {name} ({compatible})
 */
{{
  "board": "",
  "category": "{category}",
  "compatible": ["{compatible}"],
  "properties": {{
    "reg": {{ "type": "int", "description": "I2C/SPI address"}}
  }}
}}
"""
}

class DriverInitCommand(WestCommand):
    """Create a Zephyr driver skeleton."""

    def __init__(self):
        super().__init__(
            'driver',
            # will be 'west driver init'
            self.__class__.__name__,
            # subparser name, help
            'init', 'Scaffold a new Zephyr driver')
        self.hidden = False

    def do_add_parser(self, parser_adder):
        p = parser_adder.add_parser(
            self.name,
            help=self.help)
        p.add_argument('-n', '--name',     help='driver name, e.g. mcp7940mt')
        p.add_argument('-c', '--compatible', help='device-tree compatible string')
        p.add_argument('-b', '--bus',
                       choices=('i2c', 'spi', 'gpio'),
                       help='bus type')
        p.add_argument('-p', '--path',
                       help='where to create files (relative)')
        p.add_argument('--yes', action='store_true',
                       help='skip prompts, take defaults from flags')
        return p

    def do_run(self, args, _):
        # gather info
        info = {}
        def ask(key, prompt, default=None):
            val = getattr(args, key)
            if val or args.yes:
                return val
            return input(f"{prompt} [{default}]: ") or default

        info['name']       = ask('name', 'Driver name', 'my_driver')
        info['compatible'] = ask('compatible', 'Compatible string', 'vendor,dev')
        info['bus']        = ask('bus', 'Bus type', 'i2c')
        info['path']       = ask('path', 'Driver path', f"drivers/{info['name']}")

        # normalize
        info['category'] = f"{info['bus']}"
        info['uc_name'] = info['name'].upper()

        # create directories & files
        for template_path, content in TEMPLATE_FILES.items():
            rel = template_path.replace('__driver__', info['name']).format(**info)
            log.dbg(f"Creating {rel}")
            os.makedirs(os.path.dirname(rel), exist_ok=True)
            with open(rel, 'w', newline='\n') as f:
                f.write(content.format(**info))

        log.inf("Driver scaffold complete. Don’t forget to:")
        log.inf("  • Add CONFIG_%s=y to your prj.conf", info['uc_name'])
        log.inf("  • Overlay your device-tree with compatible \"%s\"", info['compatible'])
        return 0
