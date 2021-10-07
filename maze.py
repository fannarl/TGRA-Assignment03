from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

import pygame
from pygame.locals import *

from Shaders import *
from Matrices import *

class Maze:
    def __init__(self):
        self.grid = [[1,1,1,1,1,1,1,1,1,1],
                     [1,0,0,0,0,0,0,0,0,1],
                     [1,1,1,0,1,1,1,1,0,1],
                     [1,0,1,0,1,0,1,1,0,1],
                     [1,0,1,0,1,0,1,1,0,1],
                     [1,0,1,2,1,0,0,2,0,1],
                     [1,0,1,0,1,1,1,1,0,1],
                     [1,0,1,0,1,0,0,1,0,1],
                     [1,0,0,0,1,0,0,2,0,1],
                     [1,1,1,1,1,1,1,1,1,1],]
        
        self.model_matrix   = ModelMatrix()
        self.shader         = Shader3D()
        self.cube           = Cube()

    def drawCube(self, i, x):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(float(i), 0.0, float(x))  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        self.model_matrix.add_scale(1.0, 2.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def drawDoor(self, i, x, angle):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(float(i), 0.0, float(x))  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        self.model_matrix.add_rotate_y(self.angle)
        self.model_matrix.add_scale(0.2, 2.0, 1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def maze(self, angle):
        self.angle = angle
        for i in range(len(self.grid)):
                for x in range(len(self.grid[i])):
                    if self.grid[i][x] == 0:
                        if self.grid[i+1][x] == 1:
                            tmp_i = i+1
                            self.drawCube(tmp_i, x)
                        if self.grid[i-1][x] == 1:
                            tmp_i = i-1
                            self.drawCube(tmp_i, x)
                        if self.grid[i][x+1] == 1:
                            tmp_x = x+1
                            self.drawCube(i, tmp_x)
                        if self.grid[i][x-1] == 1:
                            tmp_x = x-1
                            self.drawCube(i, tmp_x)
                        #--------------door--------------#
                        if self.grid[i+1][x] == 2:
                            tmp_i = i+1
                            self.drawDoor(tmp_i, x, angle)
                        if self.grid[i-1][x] == 2:
                            tmp_i = i-1
                            self.drawDoor(tmp_i, x, angle)
                        if self.grid[i][x+1] == 2:
                            tmp_x = x+1
                            self.drawDoor(i, tmp_x, angle)
                        if self.grid[i][x-1] == 2:
                            tmp_x = x-1
                            self.drawDoor(i, tmp_x, angle)
                    elif self.grid[i][x] == 2:
                        if self.grid[i+1][x] == 1:
                            tmp_i = i+1
                            self.drawCube(tmp_i, x)
                        if self.grid[i-1][x] == 1:
                            tmp_i = i-1
                            self.drawCube(tmp_i, x)
                        if self.grid[i][x+1] == 1:
                            tmp_x = x+1
                            self.drawCube(i, tmp_x)
                        if self.grid[i][x-1] == 1:
                            tmp_x = x-1
                            self.drawCube(i, tmp_x)