'''
    Traite les résultats théoriques
    En traçant des graphes
'''


import numpy as np
import matplotlib.pyplot as plt



angle = {
        0 : [0.667,1.28,2.29,3.57,5.03],
        10: [0.669,1.29,2.31,3.59,5.11],
        20: [0.715,1.41,2.46,3.90,5.52],
        30: [0.712,1.43,2.40,3.93,5.60],
        45: [0.629,1.30,2.16,3.27,4.81],
        60: [0.480,1.00,1.70,2.56,3.60] }

vitesse = [10,15,20,25,30]

# Graph avec absisse vitesse, et ordonnée Cx
plt.plot(vitesse, angle[0],  label='Angle 0°' , marker ='x')
plt.plot(vitesse, angle[10], label='Angle 10°', marker ='x')
plt.plot(vitesse, angle[20], label='Angle 20°', marker ='x')
plt.plot(vitesse, angle[30], label='Angle 30°', marker ='x')
plt.plot(vitesse, angle[45], label='Angle 45°', marker ='x')
plt.plot(vitesse, angle[60], label='Angle 60°', marker ='x')
plt.legend()
plt.xlabel('Vitesse (m/s)')
plt.ylabel('Coefficient de trainée')

plt.show()
