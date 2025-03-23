/*
  Version simplifié, 1 seul fichier est utilisé

  Code TIPE :
  - Mesure angle de l'aile
  - Mesure intensité du courant
  - Mesure vitesse

  - Ecrire sur Carte SD les données la trame :
    angle, vitesse1, vitesse2, puissance moteur
    en deg, en m/s,           en W

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

// Creation des variables globales
const int chipSelect = 10;
const float Rt = 6371000; // rayon de la Terre (m)
float u,i,v1,v2;
int j,a=0;



// =================
//      Setup
// =================
void setup() {
  Serial.begin(9600);
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
  if (!SD.begin(chipSelect)) {
    digitalWrite(cardState, HIGH);
  }
}




float vitesseGPS(){
  /* Fonction qui récupère la vitesse du GPS
     Prend 2 vitesse de l'avion:
     - Une donné par le module GPS
     - Une calculé à la main
     Pour avoir une vitesse plus précise
  */
  

  if (gps.encode(gpsSerial.read() )){
    if (gps.location.isValid()){
    // On récupère v1 :
      v1 = gps.speed.mps(); // vitesse en m/s 
    }


    // On calcul v2 :
    float t1,t2;
    float d1,d2,d;
    float v2;
    
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
    // d = sqrt(d1²+d²)
    d = pow(d1,2)+pow(d2,2);
    d = pow(d,0.5);
    
    v2 = d/(t1-t2);
  }

  return v1,v2;
}

File dataToSD(){
  // Fonction pour écrire les données sur log{i}.txt
  logFile = SD.open("log.txt", FILE_WRITE);
  if (logFile) {
    // Ecriture sur le fichier
    logFile.print(a);
      logFile.print(", ");
    logFile.print(v1);
      logFile.print(", ");
    logFile.print(v2);
      logFile.print(", ");
    logFile.println(i);
    // Fermeture du fichier
    logFile.close();
  } 
  else { // Si le fichier ne s'ouvre pas
    digitalWrite(fileState, HIGH);
  }
}




// =================
//      Looop
// =================
void loop() {
  // Lecture tension capteur effet Hall
  u = analogRead(A0);
  // Conversion en intensité du courant capté
  i = 0.39*(u-512);
  // Conversion en puissance électrique
  // Le moteur est commandé seulement en intensité
  // U = 14.8V pour du 4s
  i = 14.8*i;

  // Lecture de l'angle de l'aile
  a = analogRead(A1);
  // Conversion de byte en degrée
  a = a*270/1023;

  // Lecture de la vitesse
  v1,v2 = vitesseGPS();

  // Ecriture sur la carte SD
  dataToSD();
}
