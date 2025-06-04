'''
    Traite les résultats théoriques
    En traçant des graphes
'''


import numpy as np
import matplotlib.pyplot as plt



angle = {
        0 : [18.1, 21.9, 20.6, 20.4, 20.7],
        10: [17.5, 21.0, 19.8, 19.7, 19.8],
        20: [15.5, 17.5, 17.0, 17.3, 17.3],
        30: [14.0, 15.9, 16.1, 15.2, 15.3],
        45: [11.3, 12.5, 12.8, 13.1, 12.8],
        60: [8.19, 8.96, 9.06, 9.38, 9.58] }

vitesse = [10,15,20,25,30]

# Graph avec absisse vitesse, et ordonnée Cx
plt.plot(vitesse, angle[0],  label='Angle 0°' , marker ='x')
plt.plot(vitesse, angle[10], label='Angle 10°', marker ='x')
plt.plot(vitesse, angle[20], label='Angle 20°', marker ='x')
plt.plot(vitesse, angle[30], label='Angle 30°', marker ='x')
plt.plot(vitesse, angle[45], label='Angle 45°', marker ='x')
plt.plot(vitesse, angle[60], label='Angle 60°', marker ='x')
# plt.legend()
plt.grid()
plt.xlabel('Vitesse (m/s)')
plt.ylabel('Cz/Cx (portée/trainée)')

plt.show()
