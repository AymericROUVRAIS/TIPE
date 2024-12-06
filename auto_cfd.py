''' 
Code : Automation des simulations de fluides de l'avion
Logiciel de CFD : 
    FluidX3D (github.com/ProjectPhysX/FluidX3D)
    De Dr. Moritz Lehmann
'''



import os
import h5py # gère les fichiers h5
import numpy as np
from stl import mesh # numpy-stl




# Variable pour la simulation
angle  = [10*i for i in range(6)] # en ° (angle de l'aile)
vitesse = [] # en km/h

# Constantes - pour le calcul de meca flu
RHO = 1.225 # en kg/m³ (masse volumique de l'air)
SURFACE_AILE = 1.0# en m²
CORDE = 0 # en m (pour le calcul de Re)




# Fonctions :
def modif_stl(a):
    '''
    modif_stl(int) -> None
    Modifie le fichier stl de l'avion (complet)
    - tourne l'aile seul
    - reconstruit le fichier avec l'avion et l'aile
    '''

    # Ouvre le fichier avec seulement l'aile
    aile_mesh = mesh.Mesh.from_file('input.stl')
    a = np.radians(a)
    # Crée une matrice pour tourner l'aile
    rotation_matrix = np.array([np.cos(a), -np.sin(a), 0])
    # Crée une matrice pour faire la translation
    translation_matrix = np.array([0,0,0])                              # VALEUR A MODIFIER !!!!!
    # Tourne l'aile de {angle} rad
    aile_mesh.rotate_using_matrix(rotation_matrix)
    # Monte l'aile pour la positionner p/r à l'avion
    aile_mesh.translate_using_matrix(translation_matrix)
    aile_mesh.save(f'aile_{a}.stl')

    # Reconstruit en fichier stl avec l'avion et l'aile
    avion_mesh = mesh.Mesh.from_file('body.stl') # fichier avec seulement l'avion
    mesh_data = np.concatenate([avion_mesh.data, aile_mesh.data])
    combined_mesh = mesh.Mesh(mesh_data)
    # Sauvegarder le fichier
    combined_mesh.save(f'ad1_{a}.stl')



def changer_parametres(v,a,f):
    '''
    changer_parametres(int,int,str) -> None
    Change le fichier contenant les paramètres de la simulation
    Modifie :
        - l'angle de l'aile  (avec le fichier stl)
        - vitesse de l'avion (avec les paramètres de simulation)
    '''

    ## Creation d'un nouveau fichier stl
    modif_stl(a)

    ## Ouvre le fichier des parametres pour lire les données
    with open('template.txt','r') as para:
        data = para.read()
        # Dans les paramètres de simulation :
        # Modifie la vitesse
        # Modifie l'angle de l'aile


    ## Créer un nouveau fichier
    with open(f,'w') as file:
        file.write(data)


def lancer_simulation(f,out_f): 
    '''
    lancer_simulation(str) -> None Lance la simulation de FluidX3D
    '''
    # -i specific input file
    # -o output directory
    os.system(f'fluidx3d -i {f} -o /results/{out_f}')



# On lance les simulations pour chaque vitesse et angle
for vit in vitesse:
    for ang in angle:
        filename = f'input_speed{vit}_angle{ang}.txt'
        output_name = f'results_speed{vit}_angle{ang}.h5'
        changer_parametres(vit,ang,filename)
        lancer_simulation(filename)
