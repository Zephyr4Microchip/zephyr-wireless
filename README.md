# Zephyr-Wireless
Microchip Wireless Solutions repository to get started with Bluetooth Low Energy (LE) and OpenThread development on PIC32CX-BZx and WBZx devices. Explore sample applications, setup guides, and resources to accelerate your wireless connectivity projects on Microchip’s advanced platforms.

## Contents
1. [List of boards supported](#step1)
2. [Environment Setup](#step2)
3. [Building Sample Applications](step3)
4. [Getting Started with Applications](#step4)
5. [Getting Started with OpenOCD](#step5)

## 1. List of boards supported<a name="step1">
|Board Name| Zephyr Board Name|
| :- | :- |
|[PIC32CX-BZ2 and WBZ451 Curiosity Development Board](https://www.microchip.com/en-us/development-tool/ev96b94a) |wbz451_curiosity|
|[WBZ451HPE Curiosity Board](https://www.microchip.com/en-us/development-tool/ev79y91a) |wbz451hpe_curiosity|
|[PIC32CX-BZ2 and WBZ450 Curiosity Development Board](https://www.microchip.com/en-us/development-tool/EV22L65A) |wbz450_curiosity|
|[PIC32-BZ6 Early Access Curiosity Board](https://www.microchip.com/en-us/development-tool/ea81w68a) |pic32wm_bz6204_curiosity|

## 2. Environment Setup<a name="step2">

### VS Code IDE (Recommended for Ease of Use)
 - [Getting Started with VS Code + Workbench for Zephyr](./docs/Workbench_for_Zephyr.md)

### Legacy Command Line
- Setup the zephyr environment by following the [Getting Started Guide — Zephyr Project Documentation link](https://docs.zephyrproject.org/latest/develop/getting_started/index.html).
- Instead of running west init to initialize a workspace based on the default manifest, use the following command.
```bash
west init -m https://github.com/Zephyr4Microchip/zephyr.git --mr mchp_pic32cxbz_v420 zephyrproject/
cd zephyrproject
west update
```
- Resume the steps in [Getting Started Guide — Zephyr Project Documentation link](https://docs.zephyrproject.org/latest/develop/getting_started/index.html).
- Before building the Blinky Sample, run the following command to fetch the required libraries.
```bash
west blobs fetch hal_microchip
```

## 3. Building Sample Applications<a name="step3">
- Build the Blinky with west build for WBZ451 Curiosity
```bash
cd zephyr
west build -p always -b wbz451_curiosity samples\basic\blinky
```
## 4. Getting Started with Applications<a name="step4">
- [Bluetooth LE Applications](./docs/Bluetooth%20LE%20Applications.md)
- [Open Thread Applications](./docs/Openthread_Sample_Applications.md)

## 5. Getting Started with OpenOCD<a name="step5">
- Refer the [Getting Started with OpenOCD](./docs/Getting_Started_with_OpenOCD.pdf)
