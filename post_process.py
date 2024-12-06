'''
Code : Traitement après la génération par CFD
Fichiers générer : en HDF5 (.h5)
Utilise les résultats de auto_cfd.py
'''


import matplotlib as plt
import numpy as np
import h5py # gère les fichiers h5
from auto_cfd import * # importer les fonctions de auto_cfd.py




def traitement(filename):
    '''
    traitement(str) -> (float,float)
    Traite les fichiers générer par FluidX3D
    Retourne la force de trainée et de pousée
    '''

    with h5py.open(filename, 'r') as h5file:
        force_x = np.array(h5file['/forces/x'])
        force_y = np.array(h5file['/forces/y'])
    # Calcul des forces
    force_trainee = np.sum(force_x)
    force_poussee = np.sum(force_y)

    return np.mean(force_trainee),np.mean(force_poussee)


def calcul_coeff(vitesse,force_trainee,force_pousee):
    '''
    post_process(int,float,float) -> (float,float)
    Calcul les coefficients de poussée et trainée
    '''

    c_t = 2*force_trainee / (RHO*SURFACE_AILE* vitesse**2)
    c_p = 2*force_trainee / (RHO*SURFACE_AILE* vitesse**2)

    return (c_t,c_p)


def angle_optimal(v_fixe):
    '''
    angle_optimal(list) -> int
    Cherche l'angle optimal pour une vitesse donnée
    '''

    # Recherche de c_t minimal
    min_c = v_fixe[0][1]
    a = v_fixe[0][0]
    for el in v_fixe:
        if el[1] < min_c:
            min_c = el[1]
            a = el[0]
    return a



# Constantes - pour le calcul de meca flu
RHO = 1.225 # en kg/m³ (masse volumique de l'air)
SURFACE_AILE = 1.0# en m²
CORDE = 0 # en m (pour le calcul de Re)

# Résultat de la simulation
resu = {} # de la forme {vitesse : (angle, c_t, c_p)}
opti = {} # de la forme {vitesse : angle_optimal}

for v in vitesse:
    for a in angle:
        # Exporter les données
        (f_t, f_p) = traitement(f'results_speed{v}_angle{a}.h5')
        resu[v] = calcul_coeff(a,f_t,f_p)


    # Calcul pour trouver l'angle optimal
    opti[v] = angle_optimal(v)


# Tracage de l'angle optimal en fonction de v
list_y = [opti[v] for v in vitesse]
plt.plot(vitesse,list_y)
plt.title('Angle optimal de l\'aile en fonction de la vitesse')
plt.grid(True)
plt.show()
