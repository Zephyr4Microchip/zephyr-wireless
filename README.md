# Zephyr-Wireless
Microchip Wireless Solutions repository to get started with Bluetooth Low Energy (LE) and OpenThread development on PIC32CX-BZx and WBZx devices. Explore sample applications, setup guides, and resources to accelerate your wireless connectivity projects on Microchip’s advanced platforms.

## Contents

1. [List of boards supported](#step1)
2. [Environment Setup](#step2)
3. [Getting Sarted with Applications](#step3)
4. [Getting Started with OpenOCD](#step4)

## 1. List of boards supported<a name="step2">

1. [PIC32CX-BZ2 and WBZ451 Curiosity Development Board](https://www.microchip.com/en-us/development-tool/ev96b94a)
2. [WBZ451HPE Curiosity Board](https://www.microchip.com/en-us/development-tool/ev79y91a)
3. [PIC32CX-BZ2 and WBZ450 Curiosity Development Board](https://www.microchip.com/en-us/development-tool/EV22L65A)
4. [PIC32-BZ6 Early Access Curiosity Board](https://www.microchip.com/en-us/development-tool/ea81w68a)

## 2. Environment Setup<a name="step3">
- Setup the zephyr environment by following the [Getting Started Guide — Zephyr Project Documentation link](https://docs.zephyrproject.org/latest/develop/getting_started/index.html).
- Instead of running west init to initialize a workspace based on the default manifest, use the following command:
```bash
west init -m https://github.com/Zephyr4Microchip/zephyr.git --mr mchp_pic32cxbz_v420 zephyrproject/
cd zephyrproject
west update
west blobs fetch hal_microchip
```

## 3. Getting Sarted with Applications<a name="step3">
- [Bluetooth LE Applications](./docs/Bluetooth%20LE%20Applications.md)
- [Open Thread Applications](./docs/Open%20Thread%20Applications.md)

## 4. Getting Started with OpenOCD<a name="step4">
- Refer the [Getting Started with OpenOCD](./docs/Getting_Started_with_OpenOCD.pdf)
