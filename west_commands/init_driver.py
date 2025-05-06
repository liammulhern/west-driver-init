import os
from west.commands import WestCommand

# Template definitions for scaffolding files
TEMPLATE_FILES = {
    "include/drivers/{category}/{name}.h": """
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
    "src/{name}.c": """
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
    "Kconfig": """
menu "Custom Driver Options"

config {uc_name}
    bool "Enable {name} driver"
    default n
    help
      Enable the {name} driver.  Requires CONFIG_{bus_upper}_IFACE=y.
endmenu
""",
    "CMakeLists.txt": """
zephyr_library()
zephyr_library_sources_ifdef(CONFIG_{uc_name} src/{name}.c)
zephyr_library_include_directories(include)
""",
    "dts/bindings/{category}/{compatible_file}.yaml": """
/*
 * Device tree binding for {name} ({compatible})
 */
{{
  "board": "",
  "category": "{category}",
  "compatible": ["{compatible}"],
  "properties": {{
    "reg": {{ "type": "int", "description": "I2C/SPI address" }}
  }}
}}
"""
}

def ask_value(args, key, prompt, default=None):
    """
    Return value from args.<key> or, if not present and --yes is False, prompt user.
    """
    val = getattr(args, key, None)
    if val or args.yes:
        return val
    return input(f"{prompt} [{default}]: ") or default


def render_template(template: str, info: dict) -> str:
    """
    Safely format a template with the provided info dict. Raises KeyError if missing.
    """
    return template.format(**info)


def generate_files(info: dict, templates=TEMPLATE_FILES) -> list[tuple[str, str]]:
    """
    Return a list of (relative_path, content) for all templates, rendered.
    """
    files = []
    for tpl_path, tpl_content in templates.items():
        rel = tpl_path.format(**info)
        content = render_template(tpl_content, info)
        files.append((rel, content))
    return files


def write_files(files: list[tuple[str, str]], path=""):
    """
    Create directories and write each file to disk.
    """

    for rel, content in files:
        rel = os.path.join(path, rel)
        print(rel)

        dirpath = os.path.dirname(rel)

        if dirpath:
            os.makedirs(os.path.dirname(rel), exist_ok=True)

        with open(rel, 'w', newline='\n') as f:
            f.write(content)

class DriverInitCommand(WestCommand):
    """Create a Zephyr driver skeleton."""
    @property
    def color_ui(self):
        # Disable West’s config-based color handling (avoids recursion in tests)
        return False

    def __init__(self):
        super().__init__(
            'driver',
            'init',
            'Scaffold a new Zephyr driver')
        self.hidden = False

    def do_add_parser(self, parser_adder):
        p = parser_adder.add_parser(
            self.name,
            help=self.help)
        p.add_argument('-n', '--name', help='driver name, e.g. mcp7940mt')
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
        info['name'] = ask_value(args, 'name', 'Driver name', 'my_driver')
        info['compatible'] = ask_value(args, 'compatible', 'Compatible string', 'vendor,dev')
        info['bus'] = ask_value(args, 'bus', 'Bus type', 'i2c')
        info['path'] = ask_value(args, 'path', 'Driver path', f"drivers/{info['name']}")

        # normalize additional fields
        # extract the sub‐directory under "drivers", e.g. "rtc" from "drivers/rtc/mcp7940mt"
        info['category'] = info['path'].split(os.sep)[1]
        info['uc_name'] = info['name'].upper()
        info['bus_upper'] = info['bus'].upper()
        # filename for the DT binding: comma → underscore
        info['compatible_file'] = info['compatible'].replace(',', '_')

        # generate and write files
        files = generate_files(info)
        write_files(files, info['path'])

        self.inf("Driver scaffold complete. Next steps:")
        self.inf("  - Add CONFIG_%s=y to your prj.conf", info['uc_name'])
        self.inf("  - Overlay your device-tree with compatible \"%s\"", info['compatible'])
        return 0

