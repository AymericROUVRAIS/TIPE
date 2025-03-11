/*
  Code TIPE :
  - Mesure angle de l'aile
  - Mesure intensité du courant
  - Mesure vitesse

  - Ecrire sur Carte SD les données la trame :
    angle, vitesse1, vitesse2, puissance moteur
    en °   en m/s               en W

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

  // Initialisation de la carte SD
  if (!SD.begin(chipSelect)) {
    digitalWrite(cardState, HIGH);
  }
  
  // Faire un nouveau fichier log
  char fileName[20];
  jTxt = SD.open("i.txt", FILE_WRITE);
  int j = lireDerniereLigne().toInt();
  jTxt.close();

  sprintf(fileName,"log%d.txt",j); // modifie fileName à log{j}.txt
  logFile = SD.open(fileName, FILE_WRITE);
  // Modifie i.txt
  if (logFile){
    logFile.println(j);
    logFile.close();
  }
  else { // Si le fichier ne s'ouvre pas
    digitalWrite(fileState, HIGH);
  }

}



String lireDerniereLigne(){
  // Fonction pour lire la derniere ligne d'un fichier de la carte SD
  logFile = SD.open("j.txt", FILE_READ);

  if (logFile) { // Si le fichier s'ouvre
    String lastLine = "";    // variable pour la dernière ligne
    String currentLine = ""; // variable pour lire chaque ligne

    // Lit le fichier charactère par charactère
    while (logFile.available()) {
      char c = logFile.read();

      if (c == '\n') {
        // On a atteint le bout d'une ligne
        lastLine = currentLine; // update la derniere ligne
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

    logFile.close();

    return lastLine;
  
  } 
  else { // Le fichier ne s'ouvre pas
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
    if (gps.location.isValid()){
    // On récupère v1 :
      v1 = gps.speed.kmph(); // vitesse en km/h
    }
  
    // On calcul v2 :
    t1 += gps.time.hour()*3600;
    t1 += gps.time.minute()*60;
    t1 += gps.time.second();
    d1 = pow(gps.location.lat(),2)-pow(gps.location.lng(),2);
    d1 = pow(d1,0.5);
        delay(100); // en ms
    t2 += gps.time.hour()*3600;
    t2 += gps.time.minute()*60;
    t2 += gps.time.second();
    d2 = pow(gps.location.lat(),2)-pow(gps.location.lng(),2);
    d2 = pow(d2,0.5);

    v2 = (d1-d2)/(t1-t2);
  }
  return v1,v2;
}

File dataToSD(){
  // Fonction pour écrire les données sur log{i}.txt
  logFile = SD.open("log.txt", FILE_WRITE);
  if (logFile) {
    // Ecriture du fichier
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
  v = vitesseGPS();

  // Ecriture sur la carte SD
  dataToSD();
}
