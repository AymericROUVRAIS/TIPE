'''
    Code pour creer fichier csv de l'arduino
    Format :
     angle, Um, I, vitesse
'''

import csv
import random as rd
import numpy as np



def post_process(file):
    '''
    post_process(String) -> None
    Prend le fichier :
        calcul la puissance a tout instant
        Garde la vitesse de la trame NMEA
    '''
    with open(file, 'r', encoding='UTF-8') as f:
        myf = f.read()
        print(type(myf))

    # Fichier post en csv
    txt_to_csv(file)

def txt_to_csv(file):
    '''txt_to_csv(String) -> None'''
    with open(file, 'r', encoding='UTF-8') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open('log.csv', 'w', encoding='UTF-8') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)



def create_trame():
    '''
    create_trame() -> dict(str)
    Creer une table de trame NMEA :
        heure, A(=valide), lat,dir_lat, long,dir_long, vitesse, cap, date, decl.magn., checksum
    '''

    trame=[]
    for i in range(100):
        tmp = '$GPRMC,225446,A,4916.45,N,12311.12,W,'
        tmp += str(5*np.log(i+2)) +'000.5,054.7,191194,020.3,E*68'
        trame += [tmp]
    return trame

def create_i():
    '''create_i() -> dict(int)'''
    i =[]
    for j in range(100):
        i+=[rd.randint(30,40)]
    return i

def create_txt(a,i,tr):
    '''
    create_txt(a:int, v:float) -> None
    Format : angle, Um, I, vitesse
    '''
    with open('log.txt', 'w', encoding='UTF-8') as f:
        for j in range(100):
            f.writelines(str(a)+',12,'+str(i[j])+','+tr[j])





#### Code artifiel ####

# Création des variables
tr = create_trame()
i = create_i()
A = 40  #degrée

# Génération du fichier texte
create_txt(A,i,tr)


#### Code utile ####

# Generation du fichier final
post_process('log.txt')
