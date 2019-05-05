import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    color = [0, 0, 0]
    normalize(light[0])
    normalize(view)
    normalize(normal)
    a = calculate_ambient(ambient,areflect)
    d = calculate_diffuse(light,dreflect,normal)
    s = calculate_specular(light,sreflect,view,normal)
    color = [a[0] + d[0] + s[0],a[1] + d[1] + s[1],a[2] + d[2] + s[2]]
    return limit_color(color)

def calculate_ambient(ambient, areflect):
    a = [0,0,0]
    for i in range(3):
        a[i] = ambient[i] * areflect[i]
    return a

def calculate_diffuse(light, dreflect, normal):
    a = [0,0,0]
    for i in range(3):
        a[i] = light[1][i] * dreflect[i] * (dot_product(normal, light[0]))
    return a

def calculate_specular(light, sreflect, view, normal):
    a = [0,0,0]
    for i in range(3):
        stuff = dot_product(subtract(multiple_constant(multiple_constant(normal, 2), (dot_product(normal, light[0]))) , light[0]) , view)
        if stuff < 0 and SPECULAR_EXP % 2 is 0:
            stuff = -1 * math.pow( stuff, SPECULAR_EXP)
        else:
            stuff = math.pow(stuff, SPECULAR_EXP)
        a[i] = light[1][i] * sreflect[i] * stuff
    return a

def multiple_constant(light, constant):
    return [light[0] * constant, light[1] * constant, light[2] * constant]
def subtract(a,b):
    return [a[0] - b[0], a[1] - b[1], a[2] - a[2]]
def multiple_vector(light, vector):
    for i in range(3):
      light[i] = light[i] * vector[i]
    return light

def limit_color(color):
    for i in range(3):
      if color[i] > 255:
        color[i] = 255
      if color[i] < 0:
        color[i] = 0
      color[i] = int(color[i])
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude
    return vector

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
