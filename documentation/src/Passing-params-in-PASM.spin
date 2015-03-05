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
        add         addr,       #4      ' Increment addr by 1 byte
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
