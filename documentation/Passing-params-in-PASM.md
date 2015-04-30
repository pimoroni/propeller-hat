<!--
---
title: Passing params in Propeller Assembly
handle: passing-params-propeller-pasm
type: tutorial
summary: A detailed guide to passing one or more params into a Propeller Assembly ( PASM ) program running on Propeller HAT.
author: Phil Howard
products: [propeller-hat]
tags: [Propeller HAT, Raspberry Pi, Microcontroller, PASM, Programming]
images: [images/tba.png]
difficulty: Advanced
-->
#Passing params in PASM

This example shows you how to pass a start address for a set of paramaters to your new Cog as the boot parameter. You can
then read each paramater, as a long or a byte, by incrementing the supplied Address and using the rdlong and rdbyte instructions
to retrieve them from the Hub.

This is a pretty standard way to bootstrap your Cog with all the information it needs to do its job, and is also a handy way
to provide arrays or single memory locations where the Cog can deposit the result of its work.

For example, you could define a LENGTH var, followed by a LED_PATTERN var and produce code in PASM which reads each byte from
LED_PATTERN in turn and flashes the LEDs. Perhaps we'll cover such a thing later.

For now, a simple example:

```spin
CON
  _CLKMODE = xtal1 + pll16x
  _XINFREQ = 6_000_000
  
VAR
  long MY_PIN_1, MY_PIN_2 ' These will appear next to each other in memory
  
PUB main
  MY_PIN_1 := |< 0		       ' Set our first pin to a bitmask for A0
  MY_PIN_2 := |< 1		       ' And our second for A1
  cognew(@blink, @MY_PIN_1)            ' Supply the address of the first parameter  
  
DAT
        org         0
blink   mov         addr,       par     ' Load our address from the boot param
        rdlong      Pn,         addr    ' Read the first pin number
        add         addr,       #4      ' Increment addr by 1 long ( 4 bytes )
        rdlong      Pn2,        addr    ' Read the second pin number
        
        or          dira,       Pn	' Set up pins as outputs
	or	    dira,	Pn2     ' It's good to do stuff while we're waiting
					' for the Hub to come back around, since we
					' only just synced for a rdbyte!
        
        rdlong      Delay,      #0      ' Prepare the delay
        mov         Time,       cnt	' Prep the wait time
        add         Time,       #9	' Add the minimum wait time
        
:loop   waitcnt     Time,       Delay   ' Start blinking!
        xor         outa,       Pn
        xor         outa,       Pn2
        jmp         #:loop
        
Pn      res         1			' Store our first LED pin
Pn2     res         1			' Store our second LED pin
Addr    res         1			' Store our parameter address
Delay	res	    1			' Store the delay increment
Time	res	    1			' Store the current time for wait
        fit
```

####Breaking it down

I'm going to assume you've read [My First Pasm](/documentation/My-first-PASM.md) and skim over much of the basics.

`long MY_PIN_1, MY_PIN_2`

In our PASM code, we're declaring two variables next to each other. These will appear adjacent to each other in HUB memory as two sets of 4 bytes, or 2 longs. These are the longs we want to copy to our COG!

```
MY_PIN_1 := |< 0
MY_PIN_2 := |< 1
```

In our `main` method, we're setting the values of `MY_PIN_1` and `MY_PIN_2` to be bit masks, by using our old friend the bitwise decode operator `|<`. Practically speaking, this will convert `0` to `%0` and `1` to `%10` etc.

We use bit masks because these can be `or`'d against our output registers to flip those bits to 1. Or `xor`d to toggle them.

It's worth noting that in SPIN and PASM you use `%` to denote a binary number, like `%10101010` and `$` to denote a hexadecimal number like `$AA`.

`mov addr, par`

The very first line of our PASM ( remember that "blink" in this case is a label, and not part of the instruction ) deals with
the `par` register. This register always starts off containing the parameter that's passed into it via `cognew`.
In this case we've passed it the Hub address of `MY_PIN_1`, and it can use this address to locate that value in the Hub when it
wants to read it. 

`rdlong      Pn,         addr`

The second line executes what's known as a HUB instruction. The instruction `rdlong` waits for the HUB to come around, then reads a long ( 4 bytes ) into the target location. In this instance Pn is our memory location within the COG and is where we want to copy the value of `MY_PIN_1`.

`add         addr,       #4`

Now that we've read one long from HUB memory, we want to advance to the next one. Addresses are byte-aligned, which means we can read one byte at a time. Since we want the next 4 bytes, and not just the last 3 of the previous long plus the first of the next long, we'll increment our `addr` register by 4. 4 bytes = 1 long.

`rdlong      Pn2,        addr`

Now we've got a pointer to `MY_PIN_2`, which is a long in memory right next to `MY_PIN_1` we can use the `rdlong` instruction to read it into `Pn2`.

Hooray. We've successfully copied two setting values from HUB memory into our COG!

`or          dira,       Pn`

In this next line we're simply `or`ing the value of `Pn` against `dira`- this sets it as an output. The bit that's set in the `Pn` mask will flip to 1 in the output register. For example `0000 or 0100 = 0100`.

Everything else you should remember from [My First Pasm](/documentation/My-first-PASM.md), we set up a loop using `waitcnt` and `jmp` and use `xor` ( `1 xor 1 = 0, 0 xor 1 = 1` ) to blink the LEDs.
