#include <SoftwareSerial.h>
#include <TinyGPS++.h>

// The serial connection to the GPS module
TinyGPSPlus gps;
SoftwareSerial gpsSerial(8,9);

float t1,t2,v;
double d1,d2;

void setup(){
  Serial.begin(9600);
  Serial.println("Setup done");
}

void loop(){
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())){
      t1 += gps.time.hour()*3600;
      t1 += gps.time.minute()*60;
      t1 += gps.time.second();
      d1 = pow(gps.location.lat(),2)-pow(gps.location.lng(),2);
      d1 = pow(d1,0.5);
        delay(50);
      t2 += gps.time.hour()*3600;
      t2 += gps.time.minute()*60;
      t2 += gps.time.second();
      d2 = pow(gps.location.lat(),2)-pow(gps.location.lng(),2);
      d2 = pow(d1,0.5);

      v = (d1-d2)/(t1-t2);
      Serial.print("Vitesse : ");
      Serial.println(v);
    }
  }
}