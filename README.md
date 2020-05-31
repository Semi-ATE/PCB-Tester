# PCB-Tester

A `PCB-Tester` is a base setup that is used to test a PCB.

The tool is used by OEM's either in new production and/or repair.

The PCB-Tester project implements such a `PCB-Tester` in open source.

It consists out of the following components:

* Rack ➜ 19", holds the 'instruments' of choice when implementing a tester for a specific PCB
* Housing ➜ The 'box' that holds the PCB-Tester (1x [PCB-Tester-Board](https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Tester-Board) and 0 or more [PCB-Relay-Boards](https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Relay-Board))
* Fixture ➜ mounted on the `Housing`, and implements the "moving mechanics"
* JIG ➜ not part of this project, belongs to a specific implementation. (iow: 'needle-bed')

The whole thing looks like this:

 ![PCB-Tester](/documentation/pictures/PCB-Tester.png)

# Wiki

Further reading at the project's [wiki](https://github.com/ate-org/PCB-Tester/wiki).
