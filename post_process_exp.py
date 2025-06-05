'''
    Code TIPE : Traitement des données expérimentales
    - Récupère les données de log.txt
      les résultats expérimentaux donnés par la carte Arduino. 
      Les fichiers log sont de la forme:
          angle, vitesse, intensité
                 mesuré   moteur
          angle, ...
          ...
        {angle1 : [(vitesse1, vitesse2, puissance moteur)] }

    satellite | lat,long | vitesse(m/s) | hdop | course | alt | date | time | angle / intensité


    - Trace l'evolution de l'intensité en fonction
      de la vitesse à un angle donné
'''






import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


# Python prend ~ comme un caractère et non pas un raccourci
file = 'log.txt'
with open(file, 'r', encoding='UTF-8') as f:
    lines = [line.split(',') for line in f]





# On garde les vitesses et intensité
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





# Conversion en matrice pour plt.errorbar()
x = np.array(vitesses[4:])
intensites_exp = np.array(intensites_exp[4:])
u_exp = np.array(u_exp[4:])


# Traçage du graph
plt.errorbar(x,intensites_exp,yerr=u_exp,fmt='-x',ecolor='black',capsize=5, label='Angle de 0°')
plt.errorbar(vit1,int1,yerr=u1,fmt='-x',ecolor='black',capsize=5, label='Angle de 45°')

plt.xlabel('Vitesse (m/s)')
plt.ylabel('Intensité (A)')
plt.axis([4.,28. , 4.,45.]) 
plt.legend()

# Ajustement de la grille de cadrillage
plt.minorticks_on()

plt.grid(which='major', linestyle='-', linewidth=0.75)
plt.grid(which='minor', linestyle=':', linewidth=0.5)

# Major ticks : grand cadrillage
plt.gca().xaxis.set_major_locator(MultipleLocator(5))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
# Minor ticks : petit cadrillage plus précis
plt.gca().xaxis.set_minor_locator(MultipleLocator(1))
plt.gca().yaxis.set_minor_locator(MultipleLocator(1))

plt.grid()
plt.show()

