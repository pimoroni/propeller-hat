#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <signal.h>

#include <wiringSerial.h>
#include <wiringPi.h>

#include <sys/stat.h>

int fd;
FILE* fp;
int i;

void cleanup(void){
  serialPrintf(fd, "%cSDMP", 13);
  for(i = 0; i < 25; i++){
    serialPutchar(fd,0);
  }
  fclose(fp);
  serialClose(fd);
}

void sigintHandler(int sig_num){
  cleanup();
  exit(1);
}

int main( int argc, char *argv[] ){
  
  int playrate = 1000.0/50.0;

  fprintf(stdout,"SIDcog Serial Player\n");
  fflush(stdout);

  if( argc < 2 ){
    fprintf(stdout, "Usage: %s <filename>", argv[0]);
    return 1;
  }

  if( argc > 2 ){
    float rate = atof(argv[2]);
    if(rate > 460){
      fprintf(stdout, "Warning, max play rate is 460 updates/sec\n");
      rate = 460;
    }
    playrate = 1000.0 / rate;
  }

  fp = fopen(argv[1], "rb");

  fd = serialOpen("/dev/ttyAMA0",115200);

  fprintf(stdout,"Serial Opened\n");
  fflush(stdout);

  char buf[26];

  signal(SIGINT, sigintHandler);

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

  cleanup();

  return 0;
}
