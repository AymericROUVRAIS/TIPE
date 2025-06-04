'''
    Code TIPE : Traitement des données expérimentales
    - Récupère les données des log{i}.txt
      des résultats expérimentaux donnés par la carte
      Arduino. Fichier log de la forme:
          angle, vitesse, vitesse2, puissance
                 mesuré   calculé   moteur
          angle, ...
          ...
    - Créer une base de données sous la forme:
        {angle1 : [(vitesse1, vitesse2, puissance moteur)] }
    - Cherche le meilleur angle pour une vitesse donnée

    satellite | lat,long | vitesse(m/s) | hdop | course | alt | date | time | angle / intensité


    - Trace l'evolution de l'angle idéal en fonction
      de la vitesse
'''



# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict



# Définitions des fonctions
def traitement(i):
    '''
    traitement(int) -> dict(int : list), list
    Prend le fichier log{i}.txt
    Renvoi :
        un dictionnaire sous la forme : 
        {angle1 : [(vitesse1,vitesse2,Puissance), ...]} 
        et une liste [ecart1,ecart2,...]
    '''


    # Lecture du fichier
    file_name = 'log' + str(i) + '.txt'
    try:
        with open(file_name, 'r', encoding='UTF-8') as f:
            lines = [line.split(',') for line in f]
    except :
         print('File not found : ' + file_name)
         return None

    # Conversion de lines en dictionnaire
    dict_angle = {}
    eps = []

    for l in lines:
        v = (l[1] + l[2])/2   # moyenne des vitesses
        eps += abs(l[1]-l[2]) # l'écart entre les vitesses
        
        # On regarde si l'angle est déjà dans le dictionnaire
        if l[0] in d:
            dict_angle[ l[0] ] = [(v,l[3])]
        else :
            dict_angle[ l[0] ] += [(v,l[3])]
    
    return dict_angle,eps




def cherche_angle(d):
    '''
    cherche_angle(d) -> list

    Cherche le meilleur angle pour une vitesse donné
    Renvoi : [(vitesse: angle), ...]
    '''
    
    vit = {}
    for key, value in d.items():
        # On cherche la puissance minimal pour un angle constant
        min_p = float('inf')
        v_atteint = 0
        a_atteint
        for el in value:
            if el[2] < min_p:
                min_p = el[2]
                v_atteint = el[1]
                a_atteint = el[0]

        if not(v_atteint in vit):
            vit[v_atteint] = (a_atteint,min_p)
        else: # On a déjà une puissance minimal
            if min_p < vit[v_atteint][1]: 
                # On a une meilleur puissance minimal
                # On remplace l'ancienne valeur
                vit[v_atteint] = (a_atteint,min_p)
    
    # On veut une liste sans min_p
    vit_l = []
    for key,value in vit.items():
        vit_l = (key,value[0])
    # On trie la liste pour les vitesses croissantes
    vit_l.sort(key = lambda x:x[0])
    return vit_l






############## Boucle principale ##############



# Creation d'un default dict: dictionnaire python plus puissant
# Ici, il sert seulement à fusionner des dictionnaires facilement
angle = defaultdict(list)

# Incertitude de vitesse : ou avec Monte-Carlo et incertitudes positions
# Incertitude type A
ecart_global = [] 


# u(v) = sqrt(1/(N-1) SUM_i (v_i-v_moy)**2)


# Iteration sur tout les fichiers logs
# for i in range(2):
#     angle_i,ecart = traitement(i)
#    
#     ecart_global.append(ecart)
#
#     # On fusionne angle_i avec angle
#     for key,value in d.items():
#         angle[key].append(value)
#
# print(f'Ecart de vitesse : min {min(ecart)} km/h, max {max(ecart)} km/h')


# On cherche une le meilleur pour une vitesse donnée
# v = cherche_angle(angle)


# Traçage du graphe de l'angle en fonction de la vitesse




# Barre d'erreurs
err = []
# On affiche seulement quelques incertitudes
for i in range(len(v)//100):
    err += [ecart_global / (len(v)**0.5)]
    err += [0 for i in range(len(v))]

plt.plot(v[:][0],v[:][1], xerr=err, marker='x')
plt.title('Evolution de l\'angle optimal en fonction de la vitesse')
plt.xlabel('Vitesse (m/s)')
plt.ylabel('Angle (degré)')
plt.show()

