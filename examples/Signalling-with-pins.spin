{
 This example demonstrates signalling to another Cog using an IO pin.
 Using an IO pin to communicate with another Cog is a great way to short-
 circuit the delays incurred by communicating through the Hub.
 
 It also introduces the "waitpeq" command.
 
 waitpeq takes three arguments, the first is the state we desire from each
 pin being monitored.
 
 The second is the mask, indicating which pins should be monitored ( 1 =
 monitor, 0 = don't care ).
 
 The third is the port to monitor, on the Propeller this will always be 0
 for PORT A.
 
 The mask and state values are supplied as bitmasks a maximum of 32 bits (
 for the 32 IO pins ) long, but can be shorted if you're only interested in,
 for example, pins 0 to 4.
 
 For example:
 waitpeq(%1000,%1000,0) would wait for pin 4 to go HIGH
 and:
 waitpeq(%10000000_00000000,%10000000_00000000,0)
 would wait for pin 15 to go HIGH.
 
 For the sake of sanity, these can usually be abbreviated in different ways:
 
 waitpeq(|< 15,|< 15,0) is equivilent to the above.
 
 And so is:
 
 waitpeq(1<<15,1<<15,0)
 
 If you're familiar with the << bit-shifting operator it's probably the easiest,
 but the bitwise decode "|<" is handy if you wish to turn a value from 0-31 into
 a bitmask with a single bit set in that position.
 
}
CON
  _CLKMODE = xtal1 + pll16x
  _XINFREQ = 6_000_000

  MY_LED_PIN = 0 ' Use pin A0
  SECOND_PIN = 1 ' Use pin A1
  SIGNAL_PIN = 2 ' Use pin A2

VAR
  long stack[128] ' Allocate 128 longs of stack space for our new COG

PUB main
  cognew(await_signal, @stack) ' Start a new COG

  DIRA[MY_LED_PIN] := 1
  DIRA[SIGNAL_PIN] := 1 ' Set our signal pin to an output

  repeat ' Repeat forever
    OUTA[SIGNAL_PIN] := 1   ' Signal 1 to the other cog

    OUTA[MY_LED_PIN] := 1   
    waitcnt(cnt + clkfreq)  ' Wait 1 second

    OUTA[SIGNAL_PIN] := 0   ' Signal 0 to the other cog

    OUTA[MY_LED_PIN] := 0 
    waitcnt(cnt + clkfreq)  ' Wait 1 second

PUB await_signal
  DIRA[SECOND_PIN] := 1 
  
  repeat
    waitpeq(1 << SIGNAL_PIN,1 << SIGNAL_PIN,0) ' Wait for the signal pin to go high
    OUTA[SECOND_PIN] := 1     ' Turn second LED on
    waitcnt(cnt + clkfreq/10) ' Wait a tenth of a second
    OUTA[SECOND_PIN] := 0     ' Turn second LED off
    waitcnt(cnt + clkfreq/10) ' Wait a tenth of a second
