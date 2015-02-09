#Propeller HAT Serial IO

Propeller HAT Serial IO is a Python library which flashes your Propeller HAT with
a 30-pin, general purpose Serial GPIO driver.

It lets you control 30 pins from A0 to A29, setting them as Inputs or Outputs and
changing them from High to Low with simple serial commands.

##Prerequisites

Propeller HAT Serial IO doesn't require any special hardware setup.

##Usage

Propeller HAT Serial IO talks to your Raspberry Pi over serial.

###Reading Pins

Every time an INPUT pin value changes, it will report its state.
Each pin belongs in a bank of 5 pins, and all 5 of these pins will
have their state reported together. So, if 5 pins on one bank change
you will see one byte of update data, if 5 pins on 5 different banks
change you will see 5 bytes of update data.

**You can read the update data as follows:**

Bit 0 - 2 | 3  | 4  | 5  | 6  | 7 
----------|----|----|----|----|----
Bank #1-6 | p1 | p2 | p3 | p4 | p5

The first 3 highest bits ( 0b11100000 ) are the bank number, starting at
1 and ending at 6.

The last 5 bite ( 0b00011111 ) represent the state of each pin in that bank.
1 = HIGH and 0 = LOW.

So:

* Bank = (BYTE & 0b11100000) >> 5
* Pin states
  * 0 = BYTE & 0b00010000
  * 1 = BYTE & 0b00001000
  * ... and so on

**Pins are mapped into banks like so:**

Bank # | Pins
-------|-----------
1      | A0  to A4
2      | A5  to A9
3      | A10 to A14
4      | A15 to A19
5      | A20 to A24
6      | A25 to A29

###Writing Pins

To change pin direction and value, you must send a single byte
containing a 3-bit CMD on the highest 3 bits, and a 5-bit pin
number to tell the Propeller which pin to act upon.

Bit      | 7 | 6                        | 5                        | 4 to 0
---------|---|--------------------------|--------------------------|--------
Function | 0 | 0 = Direction, 1 = State | 0 = In,Low, 1 = Out,High | Number of pin to change from 0-29

* 0b00100001 = Set pin 1 to OUTPUT
* 0b01100001 = Set pin 1 to HIGH

Pins 30 and 32 are not read or written because these are used for Serial communication.

###Request FW version

Setting bit 7, the highest CMD bit, high switches to CMD mode. At
the moment this will always cause the Propeller HAT to emit the
FW_VERSION constant stored in the binary.

Bits 6 to 0 in this instance are reserved for future functionality.

##Library Reference

```python
p1.serialio.mode(pin, mode)
```

Change the mode of pin pin to either mode 1, OUTPUT or mode 0, INPUT. You can use
p1.io.OUTPUT and p1.io.INPUT constants for this.

```python
p1.serialio.write(pin,value)
```
Write a value to pin. 1 = HIGH, 0 = LOW.

```python
p1.serialio.read(pin)
```
Read a value from pin. Returns 1 if the pin is read as HIGH or 0 if it is low.

**Note:** This actually reads values from a list stored in Python, since the Propeller
automatically emits updated pin states and no explicit read command exists.

Here's a quick example of using p1.serialio in an interactive Python shell. The
-i command for Python runs in interactive mode, and the -m command will load
a specific module, in this case p1.serialio, saving typing out "import p1.serialio".

```bash
pi@raspberrypi ~ $ sudo python -im p1.serialio
Setting up Propeller HAT
Connected (version=1)
Sending code (1084 bytes)
>>> mode(2,1)
>>> write(2,1)
>>> mode(3,1)
>>> write(3,1)
>>>
```

**Note:** The Propeller does not have configurable internal pull-up/down resistors
on any of its IO pins. If you want to use an IO pin as an input, an appropriate
pull resistor is recommended to prevent it from floating.
