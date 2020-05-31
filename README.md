# PCB-Tester

A `PCB-Tester` is a base setup that is used to test a PCB.

The tool is used by OEM's either in new production and/or repair.

The PCB-Tester project implements such a `PCB-Tester` in open source.

It consists out of the following components:

* [Rack](https://github.com/ate-org/PCB-Tester/tree/master/hardware/mechanics/solidworks/rack) ➜ 19", holds the 'instruments' of choice when implementing a `PCB-tester` for a specific PCB.
* [Housing](https://github.com/ate-org/PCB-Tester/tree/master/hardware/mechanics/solidworks/housing) ➜ The 'box' that holds the PCB-Tester (1x [PCB-Tester-Board](https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Tester-Board) and 0 or more [PCB-Relay-Boards](https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Relay-Board))
* [Fixture](https://github.com/ate-org/PCB-Tester/tree/master/hardware/mechanics/solidworks/fixture) ➜ Mounted on the `Housing`, and implements the "moving parts".
* JIG ➜ **Not** a part of this project, belongs to a specific implementation. (iow: 'needle-bed')
* [The Software framework]((https://github.com/ate-org/PCB-Tester/tree/master/software)).

The whole thing looks like this:

<p align="center">
  <img src="/documentation/pictures/PCB-Tester.png">
</p>

# Wiki

Further reading at the project's [wiki](https://github.com/ate-org/PCB-Tester/wiki).
