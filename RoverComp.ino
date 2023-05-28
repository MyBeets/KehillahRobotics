// This is the code running on the computational arduino MEGA
// Comp gets radio, gyro and wind, gps
// Comp plans navs and executes them by relaying instructions to moter ardunio UNO
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h> //Needed for I2C to GNSS
#include <SparkFun_u-blox_GNSS_Arduino_Library.h>
#include <Vector.h>

const uint64_t pipes[2] = {0x54617572E9, 0x63726C665FLL}; //Send, Receive

// We have 32 byte package payload, arduino is an 8 bit architecutre, int and word is 2 bytes, long, float and double both 4 bytes, char is 1
//https://learn.sparkfun.com/tutorials/data-types-in-arduino/all
typedef struct{
  byte type; // message type, plan: 0->e, 1->s, 2->pr, 3 is set
  long base[2];//reference point for the remainder of the coordinates
  word disp[3][2];
} receivePak; //size is 1+8+12

typedef struct{
  long pos[2];//reference point for the remainder of the coordinates
  int w_dir;
  int b_dir;
} emitPak; //size is 8+2+2

void setGPS(){
  Wire.begin();
  if (GPS.begin() == false){
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1);
  }
  GPS.setI2COutput(COM_TYPE_UBX); //Set the I2C port to output UBX only (turn off NMEA noise)
  GPS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); //Save (only) the communications port settings to flash and BBR
}
void setRadio(){
  radio.begin();
  // radio.setAutoAck(true);
  radio.openReadingPipe(1, pipes[1]);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.printDetails();
  // radio.printPrettyDetails();
  radio.startListening();
}

RF24 radio(7, 8); // CE, CSN
SFE_UBLOX_GNSS GPS;
byte mode = 0;// modes: Standby:0, RC:1, Endurance:2, Station Keeping:3, Precision:4, Payload:5
long course[4*2][2];
byte index = 0; //course index 
byte course_size = 0;
double BVMG[2] = {49.3,124.4};
long latitude = 0;
long longitude = 0;
long gpsInterval = 0;
void setup() {
  Serial.begin(9600); // Pins 0,1 this is link to moter arduino
  Serial1.begin(9600); //Pins 17, 16 this is link to Gyro+wind
  setGPS();
  setRadio();
}

void leg(long start[2], long end[2], int w_dir, int w_dir){//leg adds start middle stop to course
    //w_dir is obviously the direction from which the true wind is coming
    course[course_size++] = start;
    int apparentAngle = abs(w_dir-w_dir)%180;
    if (apparentAngle < BVMG[0]){ // upwind
      // We want to get to stop only using the upwind BVMG
      //Cramer's rule
      double v1x = cos((w_dir+BVMG[0])*PI/180);
      double v1y = sin((w_dir+BVMG[0])*PI/180);
      double v2x = cos((w_dir-BVMG[0])*PI/180);
      double v2y = sin((w_dir-BVMG[0])*PI/180);
      double dx = stop[0]-start[0];
      double dy = stop[1]-start[1];
      double A = ((dx*v2y)-(dy*v2x))/((v1x*v2y)-(v1y*v2x));
      course[course_size++] = {start[0]+v1x*A,start[1]+v1y*A};
    }else if (apparentAngle > BVMG[1]){ //downwind
      double v1x = cos((w_dir+BVMG[1])*PI/180);
      double v1y = sin((w_dir+BVMG[1])*PI/180);
      double v2x = cos((w_dir-BVMG[1])*PI/180);
      double v2y = sin((w_dir-BVMG[1])*PI/180);
      double dx = stop[0]-start[0];
      double dy = stop[1]-start[1];
      double A = ((dx*v2y)-(dy*v2x))/((v1x*v2y)-(v1y*v2x));
      course[course_size++] = {start[0]+v1x*A,start[1]+v1y*A};
    }
    course[course_size++] = end;
}
void loop() {
  if (millis() - gpsInterval > 1000)
  {
    gpsInterval = millis();
    latitude = GPS.getLatitude();//y
    longitude = GPS.getLongitude();//x
  }
  int b_dir, w_dir;
  if (radio.available()) {
    receivePak instr;
    radio.read(&instr, sizeof(instr));
    status(instr);
  }
  if (mode != 0){
    int rudder = rudderRot(2,1,longitude,latitude,b_dir);
    int sail = sailRot(w_dir, b_dir);
  }
  emitPak resp;
  resp.pos = {longitude,latitude};
  resp.w_dir = w_dir;
  resp.b_dir = b_dir;
  radio.stopListening();
  radio.write(&resp, sizeof(resp));
  radio.startListening();
  delay(500);
}

void nextP(long lon, long lat){
  int r = 5;//5meter radius to play it safe
  long dy = (lat - course[index][1]);
  long dx = (lon - course[index][0]);
  if (sqrt(dx*dx+dy*dy) < r) index++;
}

int rudderRot(int rNoise, int stability, long lon, long lat, int b_dir, int rot_v){
  nextP(lon, lat);
  long dy = (lat - course[index][1]);
  long dx = (lon - course[index][0]);
  double target_angle = atan2(dy,dx)*180/PI;

  double dtheta = target_angle - b_dir;
  rot_v *= 180/math.pi *0.03;

  dtheta %= 360;
  if (dtheta > 180) dtheta = -180 + dtheta-180;
  double coeff = 2/math.pi * math.atan((dtheta)/40 - rot_v/stability);
  return -10*coeff*rNoise;
}


int sailRot(int w_dir, int b_dir){
    w_dir = w_dir - b_dir;
    if (w_dir > 180) w_dir = -180 + w_dir-180;
    return 44/90*wind;
}

void status(receivePak instr){
  // message type, plan: 0->e, 1->s, 2->pr, 3-> payload, 10 is set
  if (instr.type == 0){ //endurance
    mode = 2;
  }else if (instr.type == 1){ //station
    mode = 3;
  }else if (instr.type == 2){ //precision
    mode = 4;
    leg({longitude,latitude},{instr.base[0]+instr.disp[0][0],instr.base[1]+instr.disp[0][1]}, w_dir, w_dir);
    course_size--;
    leg({instr.base[0]+instr.disp[0][0],instr.base[1]+instr.disp[0][1]},{instr.base[0]+instr.disp[1][0],instr.base[1]+instr.disp[1][1]}, w_dir, w_dir);
    course_size--;
    leg({instr.base[0]+instr.disp[1][0],instr.base[1]+instr.disp[1][1]},{instr.base[0]+instr.disp[2][0],instr.base[1]+instr.disp[2][1]}, w_dir, w_dir);
  }else if (instr.type == 3){ //payload
    mode = 5;
  }else if (instr.type == 10){//set
    //set
    mode = 0;
  }
}
// star.setLen(instr.pos);
//  cont.setAngle(instr.pos);

//GPS methods
// long speed = myGNSS.getGroundSpeed();
// Serial.print(F(" Speed: "));
// Serial.print(speed);
// Serial.print(F(" (mm/s)"));

// long heading = myGNSS.getHeading();
// Serial.print(F(" Heading: "));
// Serial.print(heading);
// Serial.print(F(" (degrees * 10^-5)"));
// long latitude = myGNSS.getLatitude();//do remember to not poll GPS much more than 1hz
// long longitude = myGNSS.getLongitude();
// int32_t latitude = myGNSS.getHighResLatitude();
// int32_t longitude = myGNSS.getHighResLongitude();
