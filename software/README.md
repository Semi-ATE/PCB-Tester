# The PCB-Tester-Framework.

This directory and its subdirectories contain <ins>**anny and all**</ins> sources for the `PCB-Tester-Framework`.

The `PCB-Tester-Framework` is written 100% in [Python](https://www.python.org/), and it runs on the [Raspberry Pi (4b)](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) located on the [PCB-Tester-Board](https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Tester-Board).

A specific `PCB-Tester` <ins>implementation</ins> uses the [PCB-Tester-Template](https://github.com/ate-org/PCB-Tester-Template) repo as a starting point. The `PCB-Tester-Template` contains code, that once an implementation is finished (or later updated) it will create/update/publish a [conda](https://docs.conda.io/en/latest/) package (in the desired channel and with the desired environment) so the `PCB-Tester-Framework` can pick up on it, download it, and run it.

The `PCB-Tester-Framework` implements thus the [user interface](https://github.com/ate-org/PCB-Tester/blob/master/software/UserInterface.md), the [application interface](https://github.com/ate-org/PCB-Tester/blob/master/software/ApplicationInterface.md) ...


