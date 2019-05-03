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
    ambient = calculate_ambient(light,areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)
    color = [ambient[0]+ diffuse[0] + specular[0],ambient[1]+ diffuse[1] + specular[1],ambient[2]+ diffuse[2] + specular[2]]
    return limit_color(color)

def calculate_ambient(light, areflect):
    return multiple_vector(light[1],areflect)

def calculate_diffuse(light, dreflect, normal):
    normalize(light[0])
    normalize(normal)
    dot = dot_product(light[0], normal)
    # print(dreflect)
    return multiple_constant(multiple_vector(light[1],dreflect),dot)

def calculate_specular(light, sreflect, view, normal):
    normalize(light[0])
    normalize(view)
    normalize(normal)
    dot = dot_product(normal, light[0])
    result = multiple_constant(multiple_constant(normal,2), dot)
    result = [result[0] - light[0][0],result[1] - light[0][1],result[2] - light[0][2]]
    dot = dot_product(result, view)
    return multiple_constant(multiple_vector(light[1],sreflect),dot)

def multiple_constant(light, constant):
    # print(light[1][0])
    # print(constant)
    return [light[0] * constant, light[1] * constant, light[2] * constant]
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
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

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
