#Your first SPIN Program

##What is SPIN?

SPIN ( get it? Spin a Propeller? ) is the language of the Propeller chip. It's actually unique to the Propeller,
found nowhere else. Surprisingly it's also an interpreted language. This means it's not actually turned into a set of
instructions that the Propeller chip understands natively, but is actually run in a small interpreter inside the chip.

Propeller's native language is PASM, or "Propeller Assembly." It's a little beyond the scope of your Propeller HAT journey,
though, so we'll ignore it for now.

##What makes up a SPIN program?

Every SPIN program consists of functions, variables, constants and data indicated by "Block Designators". These concepts
are common to most programming languages, but SPIN is  strict about how and where they appear.

The block types in SPIN are:

* CON - Declares a block of Constants, such as LED_PIN = 1
* VAR - Declares a block of Variables, such as led_state := 0
* OBJ - Declares a block of Objects, these load external code ( a bit like Python's import ) for you to use in your program
* PUB - Declares a single public method- if you were loading your code as an object, you could call this method
* PRI - Declares a single private method- this would be hidden when loading your code as an object
* DAT - Declares a block of data, this is often used to store chunks of Propeller Assembly

The CON block is also used to declare some important settings such as the Clock Mode, and Crystal Frequency, which
let your program know what sort of environment it's running in.

A bare-bones SPIN program might look something like this:

```spin
CON
  _CLKMODE = xtal1 + pll16x
  _XINFREQ = 6_000_000
  
  MY_LED_PIN = 0
  
PUB main
  dira[MY_LED_PIN] := 1 ' Set the LED pin to an output
  
  repeat ' Repeat forever
    OUTA[MY_LED_PIN] := 1 ' Turn the LED on
    waitcnt(cnt + clkfreq) ' Wait 1 second 
                           ' cnt is the program counter, 
                           ' clkfreq is the number of clock ticks in a second
    DIRA[MY_LED_PIN] := 0 ' Turn the LED off
```

##_CLKMODE and _XINFREQ

These might look like complicated arcane magic at first, but they're really nothing to be worried about.
On Propeller HAT these two lines will always be the same.

_CLKMODE is being set with the value "xtal1 + pll16x" to state that we want to use the external crystal oscillator,
and set the system clock to its value, multiplied by 16x using the PLL<sup>1</sup>.

_XINFREQ is simply set with the frequency of the external clock. On Propeller HAT we use a 6Mhz crystal, so that's 6000000.
We use understores, which are ignored by SPIN when found in numbers, to make the big number read clearly at a glance.

##DIRA and OUTA

Behind the scenes of Arduino you'll find something very much like these.

#Further Reading

* <sup>1</sup> "PLL" stands for "Phase-locked Loop", read more about it here: http://en.wikipedia.org/wiki/Phase-locked_loop
