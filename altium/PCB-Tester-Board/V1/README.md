# altium/PCB-Tester-Board/V1

TODO:
- [ ] make the `SinglaRouting.SchDoc` similar to the one of the Relay-Board (64 relays instead of 48)
- [ ] replace J3 by a pull-down and a (non-munted) 2 pin header (put test poins from bottom on it)
- [ ] add SPI headers (X7A15T-Fabric for both SPI's here.
- [ ] remove X35
- [ ] replace J4 bu a pull-down and a (non-mounted) 2 pin header (put test poins from bottom on it)
- [ ] remove X37
- [ ] determine range resistors R10 & R11 in `ADC.SchDoc` 
- [ ] do we really need the 5V in `Controller.SchDoc` ??? ( the 3V3 should be enough no?)
- [ ] replace J1 with a pull-up and a (non-mounted 2 pin header) and add testpoints from bottom.
- [ ] add a header for the I2C initialization with an FTDI cable (aka: [C232HM-DDHSL-0](documentation/FTDI-C232HM-DDHSL-0/DS_C232HM_MPSSE_CABLE.pdf) (remember to put 2 points on SDA !!!)
