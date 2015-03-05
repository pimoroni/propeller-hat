CON
  _CLKMODE = xtal1 + pll16x
  _XINFREQ = 6_000_000
  
  MY_LED_PIN = 2
  
VAR
  long START_PIN, END_PIN ' These will appear next to each other in memory
  
PUB main
  START_PIN := |< 0
  END_PIN   := |< 8
  
  cognew(@sweep, @START_PIN)
  
DAT
            
        org         0
sweep   mov         Addr,       par         ' Load parameter into Addr
        rdlong      S_Pin,      Addr        ' Read START_PIN variabe from Hub
        add         Addr,       #4          ' Increment address pointer by 1 byte
        rdlong      E_Pin,      Addr        ' Read END_PIN variable from Hub

        mov         C_Pin,      S_Pin       ' Start at the START_PIN

        rdlong      Delay,      #0          ' Read clkfreq ( ticks per second )
        shr         Delay,      #4          ' Shift delay right 4 ( divide by 16 )

        mov         Time,       cnt         ' Read current system counter state
        add         Time,       #9

:loop   waitcnt     Time,       Delay
        or          dira,       C_Pin
        xor         outa,       C_Pin
        rol         C_Pin,      #1          ' Rotate C_Pin left one place
        cmp         C_Pin,      E_Pin wz    ' Compare C_Pin to END_PIN
if_e    mov         C_Pin,      S_Pin       ' Return to the START_PIN
        jmp         #:loop                  ' Loop!

Addr                res         1
S_Pin               res         1
E_Pin               res         1
C_Pin               res         1
Delay               res         1
Time                res         1
        fit
        

