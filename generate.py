##########################################
# _________  ___  ________  _______      #
#|\___   ___\\  \|\   __  \|\  ___ \     #
#\|___ \  \_\ \  \ \  \|\  \ \   __/|    #
#     \ \  \ \ \  \ \   ____\ \  \_|/__  #
#      \ \  \ \ \  \ \  \___|\ \  \_|\ \ #
#       \ \__\ \ \__\ \__\    \ \_______\#
#        \|__|  \|__|\|__|     \|_______|#
##########################################


'''
    Code TIPE : Création artificiel de données 
    Format :
     angle, vitesse, vitesse, P 
            mesuré   calculé
'''




import csv
import matplotlib.pyplot as plt
#import random as rd
#mport numpy as np



def post_process_raw(file):
    '''
    post_process_raw(String) -> list
    Prend le fichier des logs pur :
        Calcul la puissance a tout instant
        Garde la vitesse de la trame NMEA
    '''
    with open(file, 'r', encoding='UTF-8') as f:
        # Créer une liste avec les trames
        lines = [line.split(',') for line in f]
        print(lines[0])
        for subl in lines:
            # Retirer la trame après la vitesse
            del subl[-5:]
            # Retirer avant la vitesse
            del subl[3:-1]

    for i in range(len(lines)):
            # Calcul de puissance
            lines[i][1] = float(lines[i][1])*float(lines[i][2])
            del lines[i][2]
            # Vitesse de kts à m/s
            lines[i][2] = 1.944*float(lines[i][2])

    # Fichier post en csv
    # txt_to_csv(file)
    return lines



def post_process(file):
    '''
    post_process(String) -> dict(int : float,float)
    Prend le fichier des logs :
        renvoi un dict sous la forme :
        {angle1:[vitesse, Puissance], angle2: [vitesse, P]}
    '''
    angle = [0,20,40,60] # modifier si necessaire
    dict_angle = {}
    with open(file, 'r', encoding='UTF-8') as f:
        # Créer une liste avec les trames
        lines = [line.split(',') for line in f]

    for i in range(len(angle)):
        for subl in lines:
            # Regarde si l'angle appartient à angle[i]+/_5
            if angle[i]-5 <= subl[angle] <= angle[i]+5 :
                # Rajoute (vitesse,puissance) à l'angle
                # Changer subl[1] en 2 pour avoir v2
                dict_angle[angle[i]] += (subl[1],subl[3])
            
    # Fichier post en csv
    # txt_to_csv(file)
    return dict_angle


def txt_to_csv(file):
    '''
    txt_to_csv(String) -> None
    Transforme le fichier .txt en .csv
    '''
    with open(file, 'r', encoding='UTF-8') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open('log.csv', 'w', encoding='UTF-8') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)



def create_trame():
    '''
    create_trame() -> dict(str)
    Uniquement a but de simulation
    Creer une table de trame NMEA :
        heure, A(=valide), lat,dir_lat, long,dir_long, vitesse, cap, date, decl.magn., checksum
    '''

    trame=[]
    for i in range(100):
        # après vitesse
        tmp = '$GPRMC,225446,A,4916.45,N,12311.12,W,'
        tmp += str(5*np.log(i+2)) +',000.5,054.7,191194,020.3,E*68'
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
                f.writelines(str(a)+',12,'+str(i[j])+','+tr[j]+'\n')




def graph(tabl,angle):
        # puissance en fonction de l'angle
    plt.plot(tabl[2],tabl[1])
    plt.title(f'Angle de {angle}°')
    plt.ylabel('Puissance (en W)')
    plt.xlabel('Vitesse (en m/s)')
    plt.show()

def cherche_min(val):
    '''
        _min(dict) -> int
        Trouve la vitesse minimum lors de l'expérience
    '''
    min_tot = val[0][0]
    # Itération sur les angles un à un
    for i in range(len(val)):
        min_loc = val[i][0]
        for j in range(len(val[i])):
            v = val[i][0]
            if v < min_loc::
                min_loc = v
        if min_loc < min_tot:
            min_tot = min_loc
    return min_tot
        
def cherche_max(val):
    '''
        _min(dict) -> int
        Trouve la vitesse maximum lors de l'expérience
    '''
    max_tot = val[0][0]
    # Itération sur les angles un à un
    for i in range(len(val)):
        max_loc = val[i][0]
        for j in range(len(val[i])):
            v = val[i][0]
            if v > max_loc::
                max_loc = v
        if max_loc > max_tot:
            max_tot = max_loc
    return max_tot




#### Code Modélisation ####

# Création des variables
# tr = create_trame()
# i = create_i()
# A = 40  #degrée

# Génération du fichier texte
# create_txt(A,i,tr)



#### Code Expérience ####

# Generation du fichier final
i = 1
val = post_process(f'log{i}.txt')
# graph(val,40)

a,b = cherche_min(val),cherche_max(val)
liste_x = list(range(a,b))
for key, value in val:
    liste_y = [value[i][1] for i in range(len(value))]
    plt.plot(liste_x, liste_y)
plt.title('Puissance en fonction de la vitesse pour different angle')
plt.grid(True)
plt.show()

