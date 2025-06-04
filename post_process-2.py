import numpy as np
import matplotlib.pyplot as plt


print('''
##########################################
# _________  ___  ________  _______      #
#|\___   ___\\  \|\   __  \|\  ___ \     #
#\|___ \  \_\ \  \ \  \|\  \ \   __/|    #
#     \ \  \ \ \  \ \   ____\ \  \_|/__  #
#      \ \  \ \ \  \ \  \___|\ \  \_|\ \ #
#       \ \__\ \ \__\ \__\    \ \_______\#
#        \|__|  \|__|\|__|     \|_______|#
##########################################
''')

file = input('Fichier à traiter : ')

if file=='': # Si pas de réponse
    file = 'log_flight1.csv'
with open(file, 'r', encoding='UTF-8') as f:
    lines = [line.split(',') for line in f]


# Supprime la ligne donnant le nom des colonnnes
ref = lines[0]
del lines[0]


# On garde les vitesses et intensité en mémoire
# les vitesses sont arrondi à un entier
resultat = [(int(line[3]),line[-2]) for line in lines]

# Trie des résultats en fonction des vitesses
resultat.sort(key=lambda x : x[0])



# Calcul d'incertitude de type A
incertitudes = [] # (incertitude,nb de valeurs)

# Calcul des incertitudes sur l'intensité
for i in range(35):
    n,vit_moy = 0,0
    while resultat[j+n][0] == i and j+n < len(resultat):
        vit_moy += 
        n+=1
    vit_moy = vit_moy/n
    incertitudes += [(vit_moy)]

