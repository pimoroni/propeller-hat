{{
    Your first SPIN Program!
    Accompanying tutorial: https://github.com/pimoroni/propeller-hat/blob/master/documentation/Your-first-SPIN-program.md
    
    This program blinks pin A0 on the Propeller HAT board.
}}
CON
  _CLKMODE = xtal1 + pll16x  ' Use an external crystal multplied 16x
  _XINFREQ = 6_000_000        ' Our external crystal is 6Mhz
  
  MY_LED_PIN = 0 ' Use pin A0
  
PUB main
  DIRA[MY_LED_PIN] := 1      ' Set the LED pin to an output
   
  repeat                     ' Repeat forever
    OUTA[MY_LED_PIN] := 1    ' Turn the LED on
    waitcnt(cnt + clkfreq)  ' Wait 1 second 
                              ' cnt is the clock tick counter, 
                              ' clkfreq is the number of clock ticks in a second
    DIRA[MY_LED_PIN] := 0    ' Turn the LED off
                            
