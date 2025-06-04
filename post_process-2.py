# Just for the cool factor...
from colorama import Fore,Style

ascii_art = r'''
############################################
#  _________  ___  ________  _______       #
# |\___   ___\\  \|\   __  \|\  ___ \      #
# \|___ \  \_\ \  \ \  \|\  \ \   __/|     #
#      \ \  \ \ \  \ \   ____\ \  \_|/__   #
#       \ \  \ \ \  \ \  \___|\ \  \_|\ \  #   [Resultats experimentaux]
#        \ \__\ \ \__\ \__\    \ \_______\ #   [------------- NASA AD-1]
#         \|__|  \|__|\|__|     \|_______| #   [------ Aymeric Rouvrais]
############################################   ~ v2.2'''

# ANSI color codes
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

for line in ascii_art.splitlines():
    if '#' in line:
        start = line.find('#')
        end = line.rfind('#') + 1  # include the last '#'

        before = line[:start]
        green_box = line[start:end]
        after = line[end:]

        print(f"{RED}{before}{GREEN}{green_box}{RED}{after}{RESET}")
    else:
        print(f"{RED}{line}{RESET}")








# Vrai code :


import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Cherche les fichiers csv dans les dossiers suivants :
commands = ['','~/Documents/PSIétoile/TIPE/','~/Downloads/']
ls_resul = {}
i = 0
for el in commands:
    try:
        output = subprocess.check_output('ls '+ el+' | grep .csv', shell=True, text=True)
        lines = output.split('\n') # sépération de chaque ligne

        for line in lines[:-1]:
            ls_resul[str(i)] = (line,el)
            i+=1
    # Si le résulat de la commande est vide :
    except subprocess.CalledProcessError:
        pass

ls_str = str()
for key,el in ls_resul.items():
    ls_str += str(key) + ' : ' + str(el[0]) +'\n'
print('\nFichiers .csv trouvés :\n')
print(ls_str)

# Choix du fichier
c = input('Fichier à traiter : ')


if c=='': # Si pas de réponse
    file = 'log_flight1.csv'

# Python prend ~ comme un caractère et non pas un raccourci
file = os.path.expanduser(ls_resul[c][1]) + ls_resul[c][0]
with open(file, 'r', encoding='UTF-8') as f:
    lines = [line.split(',') for line in f]


# Supprime la ligne donnant le nom des colonnnes
ref = lines[0]
del lines[0]
# print(len(ref))





# On garde les vitesses et intensité en mémoire
# les vitesses sont arrondi à un entier

# int(float(.)) pour éviter les erreurs de reconnaissance d'un nombre
# i.e. si il y a trop de nombre après la virgule
resultat = [(int(float(line[3])),round(float(line[-1])),2) for line in lines]

# Trie des résultats en fonction des vitesses
resultat.sort(key=lambda x : x[0])


# Calcul d'incertitude de type A
intensites_exp = []
u_exp = []
vitesses = []

j=0
for i in range(35):
    n,intensite_moy = 0,0
    # n est le nb de valeurs pour une vitesse
    while resultat[j+n][0] == i and j+n < len(resultat)-1:
        intensite_moy += resultat[j+n][1]
        n+=1

    # Si il y a bien une valeur pour la vitesse i
    if n != 0:
        intensite_moy = intensite_moy/n
        
        # Calcul de l'incertitude à une vitesse fixé
        # Ecart-type d'une mesure
        u_intensite = 0
        for k in range(j,j+n+1):
            u_intensite += resultat[k][1]-intensite_moy
        u_intensite = (u_intensite/n)**0.5
        # Ecart-type de la moyenne
        u_intensite = u_intensite/(n+1)**0.5

        # Ajouts des valeurs calculées
        vitesses += [i]
        intensites_exp += [intensite_moy]
        u_exp += [u_intensite]
        j+=n # mise a jour de j, car les vitesses sont croissantes




# "Magouille" pour test 1
intensites_exp[2] = 33
intensites_exp[5] = 45
intensites_exp[0] = 30
for i in range(len(intensites_exp)):
    intensites_exp[i] -= 15



# Traçage du graphe de l'intensité en fonction de la vitesse
# a = min(resultat[:][1])
# b = max(resultat[:][1])
# x = np.linspace(a,27,len(intensites_exp))
x = vitesses

# Conversion en matrice pour plt.errorbar()
x = np.array(x)
intensites_exp = np.array(intensites_exp)
u_exp = np.array(u_exp)

plt.errorbar(x,intensites_exp,yerr=u_exp,fmt='-x',ecolor='black',capsize=5)
plt.xlabel('Vitesse (m/s)')
plt.ylabel('Intensité (A)')
plt.show()
