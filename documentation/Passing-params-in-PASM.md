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

`mov addr, par`

The very first line of our PASM ( remember that "blink" in this case is a label, and not part of the instruction ) deals with
the `par` register. This register always starts off containing the parameter that's passed into it via `cognew`.
In this case we've passed it the Hub address of MY_PIN_1, and it can use this address to locate that value in the Hub when it
wants to read it. 
