# Co Processor Application

Procedure to build and run the openthread coprocessor application can also be found at [OpenThread co-processor — Zephyr Project Documentation](https://docs.zephyrproject.org/latest/samples/net/openthread/coprocessor/README.html#openthread-coprocessor).

## Building

1. To build openthread Radio Co Processor application, which is part of zephyr repo, use the below command,
```bash
west build -p always -b wbz451_curiosity ./zephyr/samples/net/openthread/coprocessor/ -- -DCONF_FILE="prj.conf overlay-rcp.conf" -DDTC_OVERLAY_FILE="boards/wbz45x_curiosity.overlay" "-DOVERLAY_CONFIG=boards/wbz45x_curiosity.conf"
```
**Note:** Modify the board name as per the requirements
2. The openthread Radio Co Processor application is built with default configuration as in [prj.cnf](https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/net/openthread/coprocessor/prj.conf) file.
3. The output of the build will be available at location $zephyrproject$/zephyr/build/zephyr/ folder.
4. To flash the executable, use the following command.
```bash
west flash
```

## Bring up of OTBR and running the application

Procedure the bring up the OTBR is defined at [Raspberry Pi Setup Procedure](https://openthread.io/guides/border-router)..

## Configuring Openthread Radio Co-Processor Application

Following are the list of KCONFIG macros that can be modified as per user requirements in [prj.cnf](https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/net/openthread/coprocessor/prj.conf) file.
- To update the latest thread version, add the following macro to prj.cnf file

##### Openthread Thread Version
```bash
CONFIG_OPENTHREAD_THREAD_VERSION_1_4=y
```
