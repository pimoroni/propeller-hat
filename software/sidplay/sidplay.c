#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include <wiringSerial.h>
#include <wiringPi.h>

#include <sys/stat.h>

int main( int argc, char *argv[] ){

  int fd;
  int playrate = 1000.0/50.0;

  fprintf(stdout,"SIDcog Serial Player\n");
  fflush(stdout);

  if( argc < 2 ){
    fprintf(stdout, "Usage: %s <filename>", argv[0]);
    return 1;
  }

  if( argc > 2 ){
    playrate = 1000.0 / atof(argv[2]);
  }

  FILE* fp = fopen(argv[1], "rb");

  fd = serialOpen("/dev/ttyAMA0",115200);

  fprintf(stdout,"Serial Opened\n");
  fflush(stdout);

  char buf[26];

  int i;

  while(fread(buf, 1, 25, fp) == 25){
    /*
      Send the header for the beginning of
      each register packet.
      
      chr(13) + S + D + M + P
    */
    serialPrintf(fd, "%cSDMP", 13);
    /*
      Must send the buffer one char at a time
      since zeros will get interpreted as
      the termination string in Printf
    */
    for(i = 0; i < 25; i++){
      serialPutchar(fd,buf[i]);
    }
    delay(playrate);
  }

  fclose(fp);
  serialClose(fd);

  return 0;
}
