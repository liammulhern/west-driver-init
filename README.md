# west-driver-init

Scaffold Zephyr RTOS drivers via `west driver init`

## Purpose

`west-driver-init` is a West extension that streamlines the creation of a new Zephyr driver by generating a complete directory structure and file stubs (header, source, Kconfig, CMakeLists, DTS binding). 

## Features

* Interactive prompts or CLI flags for driver name, bus type, compatible string, and target path.
* Generates:

  * `include/drivers/<bus>/<driver>.h`
  * `src/<driver>.c`
  * `Kconfig`
  * `CMakeLists.txt`
  * `dts/bindings/<bus>/<driver>.yaml`
* Supports skipping prompts with `--yes` and flags.

## Installation

1. **Clone or reference via West manifest**

   Add this to your workspace’s `.west.yml`:

   ```yaml
   manifest:
     remotes:
       - name: liammulhern
         url-base: https://github.com/liammulhern
     projects:
       - name: west-driver-init
         repo-path: modules/west-driver-init
         revision: main
   ```

2. **Fetch and update**

   ```bash
   west update
   ```

3. **Install the extension**

   ```bash
   pip install -e modules/west-driver-init
   ```

## Usage

```
west driver init [OPTIONS]
```

### Arguments

* `-n, --name`
  Driver identifier (e.g. `mcp7940mt`).

* `-b, --bus`
  Bus type (`i2c`, `spi`, `gpio`).

* `-c, --compatible`
  Device-tree compatible string (e.g. `microchip,mcp7940`).

* `-p, --path`
  Destination path for files (default: `drivers/<bus>/<name>`).

* `--yes`
  Skip interactive prompts, using provided flags.

### Examples

**Interactive**

```bash
west driver init
```

**Non-interactive**

```bash
west driver init \
  --yes \
  --name mcp7940mt \
  --bus i2c \
  --compatible microchip,mcp7940 \
  --path drivers/rtc/mcp7940mt
```

## Generated Structure

After running, you’ll get:

```
drivers/rtc/mcp7940mt/
├── include/drivers/rtc/mcp7940mt.h
├── src/mcp7940mt.c
├── Kconfig
├── CMakeLists.txt
└── dts/bindings/rtc/microchip_mcp7940.yaml
```

* **Header**: Public API and register definitions
* **Source**: `DEVICE_INIT` stub and initialization function
* **Kconfig**: `CONFIG_<DRIVER_NAME>` symbol
* **CMakeLists**: Conditional build integration
* **DTS binding**: YAML schema for device tree

## Next Steps

1. Enable the driver in `prj.conf`:

   ```ini
   CONFIG_MCP7940MT=y
   ```
2. Add a board/device-tree overlay with the matching `compatible`.
3. Implement your driver logic and write tests.

