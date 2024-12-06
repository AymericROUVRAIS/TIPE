#include <SD.h>
#include <SPI.h> // SPI module necessaire pour communication avec la carte SD

File logFile;
const int chipSelect = 10;

int v=0;

void setup() {
  Serial.begin(9600);

  Serial.print("Initializing SD card...");
  if (!SD.begin(chipSelect)) {
    Serial.println("initialization failed");
  }
  Serial.println("initialization done.");


}

void loop() {  
  // Fonction pour écrire les données sur log{i}.txt
  logFile = SD.open("log0.txt", FILE_WRITE);
  if (logFile) {
    // Ecriture du fichier
    logFile.println(v);
    // Fermeture du fichier
    logFile.close();
  } 
  else { // Si le fichier ne s'ouvre pas
    Serial.println("error opening log.txt");
  }
  v += 1;

  // // re-ouvre le fichier pour lire
  // logFile = SD.open("log0.txt");
  // if (logFile) {
  //   Serial.println("log0.txt:");

  //   // Lit le fichier jusqu'à la fin
  //   while (logFile.available()) {
  //     Serial.write(logFile.read());
  //   }
  //   logFile.close();
  // }
  // else {
  //   digitalWrite(fileState, HIGH);
  // }

}