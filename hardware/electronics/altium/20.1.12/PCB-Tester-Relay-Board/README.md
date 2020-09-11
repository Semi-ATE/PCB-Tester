# PCB-Relay-Board

The PCB-Relay-Board is basically a 64:8 relay matrix extension for the PCB-Tester.

 ![PCB-Relay-Board](/documentation/pictures/PCB-Relay-Board.png)

It consists out of 2 parts :
- altium : the hardware design (schematics, libraries & layout)
- [vivado](/firmware/vivado/19.1/PCB-Relay-Board/) : the implementation of the FPGA

#TODO:
- [X] enlarge the number of relays from 48 to 64
- [X] add an extra pin to the header(s) for SDA (The FTDI-Cables need 2 contacts for the SDA)
- [X] add a header to the SPI interfaces (both on X7A15T-Fabric.schdoc)
- [X] change J3 to a pull-down and a 2 pin header for writing, (but don't put the header itself), remove the jumper X35 from the schematics.
- [X] change J4 to a pull-down and a 2 pin header for writing, (but don't put the header itself),remove the jumper X37 from the schematics.
- [X] put some text on the LED's (top overlay) indicating the voltage level.
