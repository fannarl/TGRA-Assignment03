
import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self) -> str:
        return "{ " + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + " }"

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def copy(self):
        return Vector(self.x, self.y, self.z)
    
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

class Cube:
    def __init__(self):
        self.verts = [ 0, 0, 0,  1, 0, 0,
                       1, 0, 1,  0, 0, 1,
                       0, 1, 0,  1, 1, 0, 
                       1, 1, 1,  0, 1, 1 ]

        self.inds =  [ 0, 1, 2,  2, 3, 0,  #front
                       5, 6, 7,  7, 4, 5,  #back
                       3, 2, 6,  6, 7, 3,  #top
                       0, 4, 5,  5, 1, 0,  #bottom
                       1, 2, 6,  6, 5, 1,  #right
                       3, 7, 4,  4, 0, 3 ] #left
        
        self.normals = [ 0, 0,-1,  0, 0,-1,  #front
                         0, 0, 1,  0, 0, 1,  #back
                         0,-1, 0,  0,-1, 0,  #bottom
                         0, 1, 0,  0, 1, 0,  #top
                         1, 0, 0,  1, 0, 0,  #right
                        -1, 0, 0, -1, 0, 0 ] #left

        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]

    def calculateNormals(self):
        for i in range(0, len(self.inds), 3):
            tri = [ self.inds[i], self.inds[i+1], self.inds[i+2] ]
            v1 = Point(self.verts[tri[0]*3], self.verts[tri[0]*3 +1], self.verts[tri[0]*3 +2])
            v2 = Point(self.verts[tri[1]*3], self.verts[tri[1]*3 +1], self.verts[tri[1]*3 +2])

            normal = Vector(0, 0, 0)
            normal.x = (v1.y*v2.z) - (v1.z-v2.y)
            normal.y = - ( (v2.z * v1.x) - (v2.x * v1.z) )
            normal.z = (v1.x*v2.y) - (v1.y*v2.x)

            normal.normalize()
            print(normal.x, normal.y, normal.z)

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)     

    def draw(self, shader):
        
        # shader.set_position_attribute(self.position_array)
        # ## ADD CODE HERE ##
        # shader.set_normal_attribute(self.normal_array)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.verts)

        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_BYTE, self.inds)

        glBuffer
        
        # glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        # ## ADD CODE HERE ##
        # glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        # glDrawArrays(GL_TRIANGLE_FAN, 20, 4)