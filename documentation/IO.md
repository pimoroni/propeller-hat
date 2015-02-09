#Propeller HAT IO

Propeller HAT IO is a Python library which flashes your Propeller HAT with a 28-pin,
general purpose i2c GPIO driver.

It lets you control 28 pins from A0 to A27, setting them as Inputs or Outputs and
changing them from High to Low with simple i2c commands.

##Prerequisites

Propeller HAT IO requires two female-to-female jump wires making these connections:

* SDA on the left, to A29 along the bottom
* SCL on the left, to A28 along the bottom

This connects your Propeller HAT to the Raspberry Pi i2c bus. The Pi has built-in
pull-up resistors, so you don't need to add these yourself.

##Usage

Propeller HAT IO appears on your Raspberry Pi i2c bus 1 as address 0x17 by default.

To change pin direction and value, you must write registers 0-63, and to read pin
values you must read registers 64-96.

Pins 28, 29, 30 and 32 are not read or written because these are used for Serial 
and i2c communication.

Basic example to turn on pin 0 in bash:

```bash
sudo i2cset -y 1 0x17 0 1   # Write direction register
sudo i2cset -y 1 0x17 32 1  # Write value register
```
Or to read a pin in bash:

```bash
sudo i2cget -y 1 0x17 64    # Read pin 1
```

##Library Reference

```python
p1.io.setup(i2c_address)
```

Set up the i2c address of the Propeller HAT IO firmware. Only use this if you've
changed the firmware with an i2c address to suit your purposes.

```python
p1.io.mode(pin, mode)
```

Change the mode of pin <pin> to either mode 1, OUTPUT or mode 0, INPUT. You can use
p1.io.OUTPUT and p1.io.INPUT constants for this.

```python
p1.io.write(pin,value)
```
Write a value to <pin>. 1 = HIGH, 0 = LOW.

```python
p1.io.read(pin)
```
Read a value from <pin>. Returns 1 if the pin is read as HIGH or 0 if it is low.

**Note:** The Propeller does not have configurable internal pull-up/down resistors
on any of its IO pins. If you want to use an IO pin as an input, an appropriate
pull resistor is recommended to prevent it from floating.

