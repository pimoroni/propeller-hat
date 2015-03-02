# Propeller HAT Hardware

##License

![CC BY-SA 4.0](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

Propeller HAT is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.: http://creativecommons.org/licenses/by-sa/4.0/

####This license covers:

* Propeller HAT board design and schematic layout - Propeller-HAT.brd, Propeller-HAT.sch

####This license does *not* cover:

* The Parallax Propeller chip itself<sup>1</sup>
* Supporting ICs and components used on the Propeller HAT
* Logos or silkscreen artwork

<sup>1</sup> The Parallax Propeller is licensed under the GNU GPL 3.0, you can find the HDL source to the microcontroller, plus more information, here: http://www.parallax.com/microcontrollers/propeller-1-open-source

####This license allows you to:

* Share — copy and redistribute the material in any medium or format
* Adapt — remix, transform, and build upon the material for any purpose, even commercially.

####However, you must:

* give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests we endorse you or your use.
* distribute your contributions under the same license as the original if you remix, transform, or build upon this material.

##Pinout

All Propeller IO is broken out in the horizontal pin headers. Note: The TX/RX pins, while available to the IC as general purpose IO pins normally, are tied to the GPIO of the Raspberry Pi and thus cannot be used.

Pins A29 and A28 are EEPROM SDA and SCL respectively. A 25LC512-I/P EEPROM is recommended, and will require 10K pullup resistors. Once added, the Propeller will allow uploads to EEPROM and will load its contents upon boot.

##Bill Of Materials

* 1 x P8X32A-Q44 - QFP Parallax Propeller IC
* 1 x ABLS3-6.000MHZ-D4Y-T - 6Mhz Crystal Oscillator
* 1 x AP7333-__SRG - 300mA, 3.3V Voltage Regulator
* 1 x EEPROM - for Raspberry HAT compatibility
* 1 x 40PIN Low Profile Female SMD Header
* 1 x 10K Resistor R0603
* 2 x 4.7K Resistor R0603
* 1 x 1K Resistor R0603
* 4 x 0.1uF Capacitor C0603K
* 2 x 1uF Capacitor C0603K

##Crystal

6Mhz was chosen for a conservative overclock, but should be well within the range of values a P8X32A chip can tolerate under normal hobbyist operating conditions. PropellerHAT can operate on a 4Mhz-8Mhz variant of the ABLS3 Crystal. Typical clock speeds at a PLL of 16 to 2x include:

| Xin  | 16x     | 8x    | 4x    | 2x    |
|------|---------|-------|-------|-------|
| 8Mhz | 128Mhz* | 64Mhz | 32Mhz | 16Mhz |
| 6Mhz | 96Mhz   | 48Mhz | 24Mhz | 12Mhz |
| 5Mhz | 80Mhz   | 40Mhz | 20Mhz | 10Mhz |

*Speed not supported or recommended.

* [ABLS3 Crystal Oscillator datasheet](/datasheets/Crystal-OSC-ABLS3-25529.pdf)
