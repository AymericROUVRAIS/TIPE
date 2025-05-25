/*
  Version simplifié, 1 seul fichier est utilisé
  Pour capteur à effet hall sur une phase du moteur
  Sans serial monitor

  Code TIPE : 
  - Mesure de l'angle de l'aile
  - Mesure de l'intensité du courant
  - Mesure de la vitesse p/r au sol

  - Ecrire sur Carte SD les données la trame :
    angle,  vitesse1, vitesse2, puissance moteur
    en deg, en m/s,             en W

  PIN LAYOUT cf Fritzing
  Les LEDs servent seulement a voir si un problème
  est arrivé lors de la mise en marche/de l'expérience
*/


#include <SoftwareSerial.h>
#include <TinyGPS++.h> // Module pour traduire la trame NMEA
#include <SD.h>
#include <SPI.h> // SPI module necessaire pour communication avec la carte SD


// Communication serial vers le GPS
TinyGPSPlus gps;
SoftwareSerial gpsSerial(8,9);
// Variables pour comuniquer avec les fichiers de la carte SD
File logFile;
// Variable pour retrouver la correspondance des LEDs
#define cardState   4 // RED LED    -> Allumé si problème d'écriture
#define ifileState  3 // WHITE LED  -> Allumé si problème de lecture sur i.txt
#define fileState   2 // YELLOW LED -> Allumé si problème de lecture sur log.txt


// Définition d'un Tuple
struct Tuple {
  float first;  // Premier  élément du 2-uplet
  float second; // Deuxième élément du 2-uplet
};


// Creation des variables globales
const int CHIP_SELECT = 10;
const int NUM_SAMPLES=256;
const float Rt = 6371000; // rayon de la Terre (m)
float u,i,p,v1,v2;
int j,angle=0;
Tuple v;






// =================
//      Functions
// =================
Tuple vitesseGPS(){
  /* Fonction qui récupère la vitesse du GPS 
    Prend 2 vitesse de l'avion:
     - Une donné par le module GPS
     - Une calculé à la main
     Pour avoir une vitesse plus précise
  */

  Tuple vit;

  if (gps.encode(gpsSerial.read() )){
    // v1 directement donné par le gps
    if (gps.location.isValid()){
      Serial.println(gps.speed.kmph());
      v1 = gps.speed.mps(); // vitesse en km/h
      // gps.speed.kmph() pour la vitesse en m/s

      // On calcul v2 :
      float t1,t2;
      float d1,d2,d;
      
      // 1ere mesure
      t1 += gps.time.hour()*3600; // Conversion de la date en s
      t1 += gps.time.minute()*60;
      t1 += gps.time.second();
      // lat et lng en degré
      d1 = gps.location.lat(); // d1 en degré
      d2 = gps.location.lng();

      // Attente pour la 2e mesure
      delay(100); // en ms

      // 2nd mesure
      t2 += gps.time.hour()*3600;
      t2 += gps.time.minute()*60;
      t2 += gps.time.second();
      // Calcul de la différence de degrés :
      // différence de degrés à l'instant t et t+100ms
      d1 -= gps.location.lat();
      d2 -= gps.location.lng();
      // Conversion en distance
      d1 *= Rt*d1; // en m
      d2 *= Rt*d2;
      // On calcul : d = sqrt(d1²+d²)
      d = pow(d1,2)+pow(d2,2);
      d = sqrt(d);
      
      v2 = d/(t1-t2);
    }

  vit.first = v1; // en m/s
  vit.second = v2; // en m/s
  return vit;
  }
}

File dataToSD(){
  logFile = SD.open("log.txt", FILE_WRITE);
  if (logFile) {
    logFile.print(angle); // Ecriture du fichier
      logFile.print(", ");
    logFile.print(v1);
      logFile.print(",");
    logFile.print(p);
    logFile.print(v.first);
      logFile.print(", ");
    logFile.print(v.second);
      logFile.print(", ");
  
    logFile.close();
  } 
  else {
    // Si le fichier ne s'ouvre pas
    digitalWrite(fileState, HIGH);
  }

  // re-ouvre le fichier pour lire
  logFile = SD.open("test.txt");
  if (logFile) {
    // Lit le fichier jusqu'à la fin
    while (logFile.available()) {
      Serial.write(logFile.read());
    }
    logFile.close();
  }
  else {
    digitalWrite(fileState, HIGH);
  }
}



// =================
//      Setup
// =================
void setup() {
  // Serial plus rapide pour respecter le critère de Shanon-Nyquist
  Serial.begin(9600); // inutile si le capteur n'est pas sur une phase
  gpsSerial.begin(9600);

  // Définir les LEDs
  pinMode(ifileState, OUTPUT);
  pinMode(cardState, OUTPUT);
  pinMode(fileState, OUTPUT);
  // Initialisé les LEDs
  digitalWrite(ifileState, LOW);
  digitalWrite(cardState, LOW);
  digitalWrite(fileState, LOW);

  // Initialisation de la carte SD
  if (!SD.begin(CHIP_SELECT)) {
    digitalWrite(cardState, HIGH);
  }
}



// =================
//      Loop
// =================
void loop() {
  // Si le capteur est branché sur une phase :
  // i = l'intensité d'une phase
  float sommeCarre=0; 
  for (int k=0; k<NUM_SAMPLES; k++){
    // Lecture tension capteur effet Hall
    u = analogRead(A0);
    // Conversion en intensité du courant capté
    i = 0.39*(u-512)/3;
    sommeCarre += i*i;
  }
  // Calcul de la valeur efficace de i
  i = sqrt(sommeCarre/NUM_SAMPLES);

  


  // Conversion en puissance électrique
  // Le moteur est commandé seulement en intensité
  // U = 14.8V pour du 4s
  p = 14.8*i;

  // Lecture de l'angle de l'aile
  angle = analogRead(A1);
  // Conversion de byte en degrée
  angle = 26+angle*270/1023;

  // Lecture de la vitesse
  v = vitesseGPS();

  // Ecriture sur la carte SD
  dataToSD();
}
