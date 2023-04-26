#include <RF24.h>
#include <RF24_config.h>
#include <nRF24L01.h>
// #include <printf.h>
#include <SPI.h>

const uint64_t pipes[2] = {0x63726C665FLL, 0x54617572E9}; //Send, Receive, should be flipped for radio receiver
RF24 radio(9, 10); // select  CSN and CE  pins

// We have 32 byte package payload, arduino is an 8 bit architecutre, int is 2 bytes, float and double both 4 bytes
typedef struct{
  int dir;
} controlDef;
controlDef controlPak; // as ints are 2 bytes this is a 2 byte package payload.

void resetData(){
  controlPak.dir = 0;
}

void setup() {
  radio.begin();
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MAX) ;
  radio.setChannel(0x34); // you need to check which chanels are free first
  radio.setAutoAck(false);
  radio.openWritingPipe(pipes[0]);
  resetData();

  radio.printDetails();// just prints out some usefull debug information
}

void loop() {
  radio.write(&controlPak, sizeof(controlPak));
}
