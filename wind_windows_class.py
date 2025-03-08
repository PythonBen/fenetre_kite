import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from fasthtml.common import *
import decimal
from decimal import Decimal
from fh_matplotlib import matplotlib2fasthtml

@dataclass
class Windcalc:
    real_wind: np.ndarray
    boat_vector: np.ndarray
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
    xmin: int = -30
    xmax: int = 30
    ymin: int = -30
    ymax: int = 30
    
    @matplotlib2fasthtml
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
        #plt.show()

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


app, rt = fast_app()


@rt("/info")
def info():
    s1 = " Pour dessiner la fenetre de vol on a utilisé du code python, la librairie fasthtml et matplotlib"
    s2 = " L'utilisateur doit entrer la vitesse du vent réel, la direction de la trajectoire et la vitesse du rider"
    s3 = " Le vent réel est toujours le vent venant du Nord (haut de la fenetre), cela simplifie le calcul et ne change rien au calcul de la fenetre de vol"
    s4 = " Une fois determiné le vent apparent, on trace la perpendiculaire à ce vent apparent et le demi cercle associé"
    s5 = " On trace ensuite deux autres vecteurs, la limite basse de la fenetre de vol et le bord de la fenetre de vol"
    s6 = " Le secteur entre ces deux lignes est appelé la fenetre de vol utile (en violet sur la figure)"
    s7 = " Pour plus d'information, voir le code source à mon adresse github"
    
     
    return (

            Div(
                H1('Informations sur le calcul de la fenetre de vol'),
                P(s1),
                P(s2),
                P(s3),
                P(s4),
                P(s5),
                P(s6),
                P(s7),
                P(A("github", href="https://github.com/PythonBen/fenetre_kite")),
                P(A('retour', href='/')),
                cls="container",
                style="padding-top: 10px;"
                )

           )

@rt("/")
def index():

    first_form = Form(method="post", action="/submit_form")(
    Fieldset(
        Label('Vent réel, vient du Nord (haut du la fenetre)', Input(name='real_wind_speed',placeholder="En noeuds ou km/h, par default vent du Nord",type="number",step="1",min="0",required=True)),
        Label('Trajectoire', Input(name='trajectory',placeholder="En °, par exemple 45° est la direction NE",type="number",step="5",min="0",required=True,default="45")),
        Label('Vitesse du rider', Input(name='rider_speed',placeholder="Vitesse en noeuds ou km/h du rider",type="number",step="1",min="1",required=True)),
            ),
        Button("Entrez le vent réel, la direction et vitesse du rider", type="submit")
            )
    return Titled("Calcul de la fenetre de vol d'un kite",
        Div(first_form, cls="form-container"),
        P(A('Plus d\'info', href='/info')))
    
@rt("/submit_form")
def submit(real_wind_speed: float, trajectory: float, rider_speed: float):
    real_wind_angle = 270
    try:
        Wind_instance = Windcalc(real_wind=Windcalc.polar_to_cartesian(real_wind_angle, real_wind_speed),\
                                 boat_vector=Windcalc.polar_to_cartesian(trajectory, rider_speed))
        
        real_wind = Wind_instance.real_wind
        app_wind = Wind_instance.apparent_wind
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
        #Drawing_instance.plotting()
        
    except Exception as e:
        return Div(P("Error"), P(str(e)))
    #return Div(P("Success"))
    return Div(
        Drawing_instance.plotting(),
         P(A('Retour', href='/')))

serve()