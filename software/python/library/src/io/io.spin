CON
  _clkmode = xtal1 + pll16x                                                      
  _xinfreq = 6_000_000

  SDA_pin = 27
  SCL_pin = 26

VAR
  long reg

OBJ                            
  slave : "I2C slave v1.2"

PUB Main | i          
  slave.start(SCL_pin,SDA_pin,$17) ' Start the slave object with a device address of $42
  
  ' Default all pins as inputs
  repeat i from 0 to 31
    dira[i] := 0
    outa[i] := 0
  
  ' Continuously poll the registers for changes
  ' and update output pins accordingly
  repeat
    repeat i from 0 to 27
        
      ' High 32 registers for direction  
      'reg := slave.check_reg(i+32)
      'if reg > -1
      dira[i] := slave.get(i+32) == 1
    
      ' Low 32 registers for state
      outa[i] := slave.get(i) == 1
      
      slave.put(i+64,ina[i])