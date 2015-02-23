CON
  _CLKMODE = xtal1 + pll16x
  _XINFREQ = 6_000_000 

OBJ
  sid    : "SIDcog"
  serial : "FullDuplexSerial"
  
VAR
  byte registers[25]
  
PUB main | readyToUpdateRegisters, i

  sid.start( 0, 1 )
  sid.setVolume(1)
  serial.start( 31, 30, 0, 115200 )

  dira[2..9] := %11111111
  outa[2..9] := %11111111
  
  repeat
    readyToUpdateRegisters := false  
    repeat while not readyToUpdateRegisters
      repeat while serial.rx <> 13
      if serial.rx == "S" and serial.rx == "D" and serial.rx == "M" and serial.rx == "P"
        readyToUpdateRegisters := true
    repeat i from 0 to 24
      registers[i] := serial.rx
    repeat i from 0 to 7
      outa[i+2] := registers[i] & 1
    sid.updateRegisters( @registers )
 
