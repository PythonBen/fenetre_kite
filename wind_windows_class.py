import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Windcalc:
    real_wind: np.ndarray
    boat_vector: np.ndarray
    #originx: int = 0
    #originy: int = 0
    constant_radius: int = 20

    @property
    def apparent_wind(self):
        return self.real_wind - self.boat_vector
    
    @staticmethod
    def polar_to_cartesian(angle_degree, norm):
        radians = np.radians(angle_degree)
        x = np.cos(radians) * norm
        y = np.sin(radians) * norm
        return np.array([x, y])
    
    @staticmethod
    def perpendicular_vectors(vector):
        return np.array([vector[1], -vector[0]]), np.array([-vector[1], vector[0]])
    
    @staticmethod
    def semi_circle(vector):
        alpha  = np.linspace(0, np.pi, 100)
        mx = np.cos(alpha) * vector[0] - np.sin(alpha) * vector[1]
        my =  np.sin(alpha) * vector[0] + np.cos(alpha) * vector[1]
        return mx * Windcalc.constant_radius / np.linalg.norm(vector), my * Windcalc.constant_radius / np.linalg.norm(vector)
    
    @staticmethod
    def back_limit(vector):
        v  = np.array([vector[1], -vector[0]]) * Windcalc.constant_radius / np.linalg.norm(vector)
        return v
    
@dataclass
class Drawing:
    real_wind: np.ndarray
    boat_vector: np.ndarray
    app_wind: np.ndarray
    ortho1: np.ndarray
    ortho2: np.ndarray
    mx: np.ndarray
    my: np.ndarray
    back_l: np.ndarray
    front_l: np.ndarray
    originx: int = 0
    originy: int = 0
    xmin: int = -20
    xmax: int = 20
    ymin: int = -20
    ymax: int = 20
    
    def plotting(self):
        plt.quiver(self.originx, self.originy, self.real_wind[0], self.real_wind[1], angles='xy', scale_units='xy', scale=1, color='blue', label="real wind")
        plt.quiver(self.originx, self.originy, self.boat_vector[0], self.boat_vector[1], angles='xy', scale_units='xy', scale=1, color='black', label="trajectory")
        plt.quiver(self.originx, self.originy, -self.boat_vector[0], -self.boat_vector[1], angles='xy', scale_units='xy', scale=1, color='green', label="velocity wind")
        plt.quiver(self.originx, self.originy, self.app_wind[0], self.app_wind[1], angles='xy', scale_units='xy', scale=1, color='red', label="apparent wind")
        plt.quiver(self.originx, self.originy, self.ortho1[0], self.ortho1[1], angles='xy', scale_units='xy', scale=1, color='pink')
        plt.quiver(self.originx, self.originy, self.ortho2[0], self.ortho2[1], angles='xy', scale_units='xy', scale=1, color='pink')
        plt.plot(self.mx, self.my, 'gray')
        plt.quiver(self.originx, self.originy, self.back_l[0], self.back_l[1], angles='xy', scale_units='xy', scale=1, color='purple', label="kite window ")
        plt.quiver(self.originx, self.originy, self.front_l[0], self.front_l[1], angles='xy', scale_units='xy', scale=1, color='purple')
        plt.xlim(self.xmin,self.xmax)
        plt.ylim(self.ymin, self.ymax)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Fenêtre de vol')
        plt.legend()
        plt.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

Wind_instance = Windcalc(real_wind=Windcalc.polar_to_cartesian(270, 10),\
                         boat_vector=Windcalc.polar_to_cartesian(45, 10))

real_wind = Wind_instance.real_wind
app_wind = Wind_instance.apparent_wind

print(f"real wind:{real_wind}")
print(f"velocity_wind:{-Wind_instance.boat_vector}")
print(f"apparent wind:{app_wind}")
boat_vector = Wind_instance.boat_vector
ortho1, ortho2 = Wind_instance.perpendicular_vectors(app_wind)
mx, my = Wind_instance.semi_circle(ortho1)
back_l = Wind_instance.back_limit(boat_vector)
front_l = ortho2*Wind_instance.constant_radius/np.linalg.norm(ortho2)


Drawing_instance = Drawing(real_wind=real_wind,
                           boat_vector=boat_vector,
                           app_wind=app_wind,
                           ortho1=ortho1,
                           ortho2=ortho2,
                           mx=mx,
                           my=my,
                           back_l=back_l,
                           front_l=front_l)
Drawing_instance.plotting()
