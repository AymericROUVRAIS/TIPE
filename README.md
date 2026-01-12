## Structure
Les fichiers .ino utilisés pour programmer la carte Arduino (nano) sont dans des dossiers pour les intégrer correctment dans l'environnement de développement Arduino (Arduino IDE).

Le fichier .fzz correspond au diagramme de branchement du système de prise de données basé sur une carte Arduin. Il provient du logiciel Fritzing. On peut le retrouver dans la présentation du TIPE sous forme d'image, où il peut être regardé sans avoir besoin du logiciel.

## Contenu
Il y a des versions avec et sans Serial Monitor pour réduire la charge calculatoire de la carte micro-contrôleur et augmenter la lisibilité du code qui devra être imprimer le jour de la soutenance.

Les fichiers codeGlobal et codeGlobal2 sont les versions complètes à but d'être utilisé lors des expériences. Mais par manque de temps je n'ai pas pu tester toutes les fonctionnalités. Elles utilisent un système multi-fichiers, pour que chaque test en ait un différent afin de simplifier la prise de données, 
et la gestion de ceux-ci. codeGlobal2 est seulement la versin avec le Serial Monitor pour aider au debug.

codeGlobalSimple et codeGlobalSerial sont ceux utilisé lors des expérimentations sur le système réel lors de vol. Ils ont sont une version simplifié de codeGlobal et codeGlobal2 utilisant seulement un fichiers, afin de réduire le risque d'erreur.
Le deuxième fichier correspond à la version avec le SerialMonitor.

Les deux derniers fichiers ont un nom correspondant à leur fonction, ils servent seulement à établir les parties du code de la version finale pour réduire le nombre d'erreurs à gérer lors de la conception du code. Cela permet aussi plus précisement de savoir d'où les bugs proviennent.
Leurs contenu ne reflète pas forcément l'intégration dans le code finale. Ils sont aussi à but de découvrir comment fonctionne les différents modules utilisés sur la carte microcontroleur.
