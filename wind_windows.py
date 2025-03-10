import matplotlib.pyplot as plt
import numpy as np

# project:
# 1. we want to draw the apparent wind vector given the real wind vector
# and the speed vector of the boat
# 2. then we want to build the flight kite window. It is a semi circle, its diameter line
# should be perpendicular to the apparent wind vector.
# 3. From that we can draw to additional lines, the low limit which is perpendicular to the trajectory
# and the edge of the flight window
# 5 This sector between these to lines is called  the effective wind window

def vectors(angle_degree, norm):
    radians = np.radians(angle_degree)
    x = np.cos(radians) * norm
    y = np.sin(radians) * norm
    return np.array([x, y]) 

def apparent_wind(real_wind, boat_vector):
    return real_wind - boat_vector

def perpendicular_vectors(vector):
    return np.array([vector[1], -vector[0]]), np.array([-vector[1], vector[0]])

# create a function to draw a semi circle joining the two arrow of the perpendicular vectors (pink arrows)
def semi_circle(vect_perp1):
    originx, originy = 0, 0
    constant_radius = 20
    #normv1 = np.linalg.norm(vect_perp1)
    #normv2 = np.linalg.norm(vect_perp2)
    
    alpha  = np.linspace(0, np.pi, 100)
    mx = np.cos(alpha) * vect_perp1[0] - np.sin(alpha) * vect_perp1[1]
    my =  np.sin(alpha) * vect_perp1[0] + np.cos(alpha) * vect_perp1[1]

    return mx * constant_radius / np.linalg.norm(vect_perp1), my * constant_radius / np.linalg.norm(vect_perp1)


def back_limit(boat_vector):
    constant_radius = 20
    normv = np.linalg.norm(boat_vector)
    #normva = np.linalg.norm(apparent_wind)
    if boat_vector[0] > 0:
        v  = np.array([boat_vector[1], -boat_vector[0]]) * constant_radius / normv
    elif boat_vector[0] < 0:
        v  = np.array([-boat_vector[1], boat_vector[0]]) * constant_radius / normv
    return v

def front_limit(boat_vector, ortho_vect1, ortho_vect2):
    if boat_vector[0] > 0:
        v = ortho_vect2 * 20 / np.linalg.norm(ortho_vect2)
    elif boat_vector[0] < 0:
        v = ortho_vect1 * 20 / np.linalg.norm(ortho_vect1)
    return v

def plotting(real_wind, boat_vector, ortho1, ortho2, mx, my, back_l, front_l):

    xmin, xmax = -20, 20
    ymin, ymax = -20, 20
    originx, originy = 0, 0
    apparent = apparent_wind(real_wind, boat_vector)
    plt.quiver(originx, originy, real_wind[0], real_wind[1], angles='xy', scale_units='xy', scale=1, color='blue', label="real wind")
    plt.quiver(originx, originy, boat_vector[0], boat_vector[1], angles='xy', scale_units='xy', scale=1, color='black', label="trajectory")
    plt.quiver(originx, originy, -boat_vector[0], -boat_vector[1], angles='xy', scale_units='xy', scale=1, color='green', label="velocity wind")
    plt.quiver(originx, originy, apparent[0], apparent[1], angles='xy', scale_units='xy', scale=1, color='red', label="apparent wind")
    plt.quiver(originx, originy, ortho1[0], ortho1[1], angles='xy', scale_units='xy', scale=1, color='pink')
    plt.quiver(originx, originy, ortho2[0], ortho2[1], angles='xy', scale_units='xy', scale=1, color='pink')
    plt.plot(mx, my, 'gray')
    plt.quiver(originx, originy, back_l[0], back_l[1], angles='xy', scale_units='xy', scale=1, color='purple', label="kite window ")
    plt.quiver(originx, originy, front_l[0], front_l[1], angles='xy', scale_units='xy', scale=1, color='purple')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin, ymax)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Fenêtre de vol')
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

real_wind = vectors(270,10)
print("vent reel")
print(real_wind)
boat_vector = vectors(0, 10)
print("vent vitesse")
print(-boat_vector)

app_wind = apparent_wind(real_wind, boat_vector)
print("vent apparent")
print(app_wind)
ortho_vect1, ortho_vect2 = perpendicular_vectors(app_wind)
print(ortho_vect1)
print(ortho_vect2)
mx, my = semi_circle(ortho_vect1)
back_l = back_limit(boat_vector)
front_l = front_limit(boat_vector, ortho_vect1, ortho_vect2)
#front_l = ortho_vect2 * 20 / np.linalg.norm(ortho_vect2)
plotting(real_wind, boat_vector, ortho_vect1, ortho_vect2, mx, my, back_l, front_l)
#semi_circle(ortho_vect1)
