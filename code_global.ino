/*
  Version avec Serial Monitor

  Code TIPE :
  - Mesure angle de l'aile
  - Mesure intensité du courant
  - Mesure vitesse

  - Ecrire sur Carte SD les données la trame :
    angle, vitesse1, vitesse2, puissance moteur
    en deg, en m/s,            en W

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
File jTxt;
// Variable pour retrouver la correspondance des LEDs
#define cardState   4 // RED LED    -> Allumé si problème d'écriture
#define ifileState  3 // WHITE LED  -> Allumé si problème de lecture sur i.txt
#define fileState   2 // YELLOW LED -> Allumé si problème de lecture sur log.txt

// Creation des variables globales
const int chipSelect = 10;
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

  // Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    // Serial.println("initialization failed");
    digitalWrite(cardState, HIGH);
  }
  // Serial.println("initialization done.");
  
  // Faire un nouveau fichier log
  char fileName[20];
  jTxt = SD.open("i.txt", FILE_WRITE);
  int j = lireDerniereLigne().toInt();
  jTxt.close();

  sprintf(fileName,"log%d.txt",j); // modifie fileName à log{j}.txt
  logFile = SD.open(fileName, FILE_WRITE);
  if (logFile){
    logFile.println(j);
    logFile.close();
  }
  else {
    digitalWrite(fileState, HIGH);
  }

}

String lireDerniereLigne(){
  logFile = SD.open("test.txt", FILE_READ);

  if (logFile) {
    String lastLine = "";    // variable pour la dernière ligne
    String currentLine = ""; // variable pour lire chaque ligne

    // lit le fichier ligne par ligne
    while (logFile.available()) {
      char c = logFile.read();

      if (c == '\n') {
        // On a atteint le bout d'une ligne
        lastLine = currentLine; //  lastLine
        currentLine = "";       // preparer pour la nouvelle ligne
      } else {
        // Ajoute le charactère à la ligne
        currentLine += c;
      }
    }
    // A la fin, lastLine = la derniere ligne du fichier
    if (currentLine.length() > 0) {
      lastLine = currentLine;
    }

    // Serial.print("Last line: ");
    // Serial.println(lastLine);

    logFile.close();

    return lastLine;
  
  } else {
    // Fichier ne s'ouvre pas
    // Serial.println("Error opening file.");
    digitalWrite(ifileState, HIGH);
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
    // v1 directement donné par le gps
    if (gps.location.isValid()){
      // Serial.println(gps.speed.kmph());
      v1 = gps.speed.mps(); // vitesse en m/s
      // gps.speed.kmph() pour la vitesse en km/h
    }
    // else {
    //  Serial.println("error with gps data");
    // }

    // Calcul de v2 :
    t1 += gps.time.hour()*3600;
    t1 += gps.time.minute()*60;
    t1 += gps.time.second();
    d1 = pow(gps.location.lat(),2)-pow(gps.location.lng(),2);
    d1 = pow(d1,0.5);
        delay(500); // en ms
    t2 += gps.time.hour()*3600;
    t2 += gps.time.minute()*60;
    t2 += gps.time.second();
    d2 = pow(gps.location.lat(),2)-pow(gps.location.lng(),2);
    d2 = pow(d2,0.5);

    v2 = (d1-d2)/(t1-t2);
  return v1,v2;
  }
}

File dataToSD(){
  logFile = SD.open("log.txt", FILE_WRITE);
  if (logFile) {
    // Serial.print("Writing to log.txt...");
    logFile.print(a); // Ecriture du fichier
      logFile.print(", ");
    logFile.print(v1);
      logFile.print(", ");
    logFile.println(v2);
      logFile.print(", ");
    logFile.println(i);

    
    logFile.close();
    // Serial.println("done.");
  } else {
    // Si le fichier ne s'ouvre pas
    // Serial.println("error opening log.txt");
    digitalWrite(fileState, HIGH);
  }

  // re-ouvre le fichier pour lire
  logFile = SD.open("test.txt");
  if (logFile) {
    Serial.println("test.txt:");

    // Lit le fichier jusqu'à la fin
    while (logFile.available()) {
      Serial.write(logFile.read());
    }
    logFile.close();
  }
  else {
    // Serial.println("error opening log.txt");
    digitalWrite(fileState, HIGH);
  }
}




// =================
//      Looop
// =================
void loop() {
  // lecture tension capteur effet Hall
  u = analogRead(A0);
  // conversion en intensité du courant capté
  i = 0.39*(u-512);
  // Conversion en puissance électrique
  // Le moteur est commandé seulement en intensité
  // U = 14.8V pour du 4s
  i = 14.8*i;


  // Serial.print("I : ");
  // Serial.println(i);


  // lecture de l'angle
  a = analogRead(A1);
  // conversion de byte en degrée
  a = a*270/1023;

  // lecture de la vitesse
  v = vitesseGPS();

  dataToSD();
}
