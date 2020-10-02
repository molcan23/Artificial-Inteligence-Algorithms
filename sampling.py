import random
import math
import numpy as np
from matplotlib import pyplot as plt


max_x = 150
max_y = max_z = 85

rad_narrow = 20
rad_mid = 25
rad_1st_c = 30
rad_2nd_c = 40

cX = 42.5
cY = 42.5


def in_circle(x, y, r):
    d = math.sqrt((x - cX)**2 + (y - cY)**2)
    return d <= r


# OK
def fx(x):
    x -= 80
    new_y_radius = 10 * (0.5 - 0.005 * x**2) + 20
    return new_y_radius


# OK
def triangle_up(x):
    new_y_radius = 15 + x
    return new_y_radius


# OK
def triangle_down(x):
    x = x - 140
    new_y_radius = 25 - x
    return new_y_radius


def direct_sampling(n):
    
    counter = 0
    whole = 0

    posX = []
    posY = []
    negX = []
    negY = []

    while whole < n:
        tx = round(random.random() * max_x, 2)
        y = round(random.random() * max_y, 2)
        z = round(random.random() * max_z, 2)
        
        rad = 0
        h = True

        if tx <= 5:
            rad = triangle_up(tx)

        elif (5 < tx <= 40) or (50 < tx <= 70) or (90 < tx <= 100):
            rad = rad_narrow

        elif 40 < tx <= 50:
            rad = rad_1st_c

        elif 70 < tx <= 90:
            rad = fx(tx)

        elif 100 < tx <= 110:
            rad = rad_2nd_c

        elif 110 < tx <= 140:
            rad = rad_mid

        elif 140 < tx <= 145:   # OK
            rad = triangle_down(tx)

        elif tx > 145:
            h = False
            rad = 0

        if in_circle(y, z, rad) and h:
            counter += 1
            posX.append(tx)
            posY.append(y)
            whole += 1
        elif in_circle(y, z, 42.5):
            negX.append(tx)
            negY.append(y)

            whole += 1

    # plt.scatter(posX, posY, s=0.5)
    # plt.scatter(negX, negY, s=0.5)
    plt.show()

    return counter/whole


print(direct_sampling(100000))
