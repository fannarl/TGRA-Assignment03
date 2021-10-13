
from OpenGL.GL import *
import OpenGL.GL.shaders

import numpy
# from OpenGL.GLU import *
# from math import *

import sys

import pygame
from pygame.locals import *

from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        # hide mouse and grab input
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(True)

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(1, 1, 0), Point(3, 3, 1), Vector(0, 0, 1))

        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 2
        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 100)


        #        positions        colors
        cube = [-0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
                0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
                0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                -0.5,  0.5,  0.5, 1.0, 1.0, 1.0,

                -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
                -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

        cube = numpy.array(cube, dtype = numpy.float32)

        indices = [0, 1, 2, 2, 3, 0,
                4, 5, 6, 6, 7, 4,
                4, 5, 1, 1, 0, 4,
                6, 7, 3, 3, 2, 6,
                5, 6, 2, 2, 1, 5,
                7, 4, 0, 0, 3, 7]

        indices = numpy.array(indices, dtype= numpy.uint32)

        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.shader = glCreateProgram()
        glAttachShader(self.shader, vert_shader)
        glAttachShader(self.shader, frag_shader)
        glLinkProgram(self.shader)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, 192, cube, GL_STATIC_DRAW)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 144, indices, GL_STATIC_DRAW)

        position = glGetAttribLocation(self.shader, "a_position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(self.shader, "u_color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        self.ViewMatrixLoc = glGetUniformLocation(self.shader, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.shader, "u_projection_matrix")

        glUseProgram(self.shader)
        glUniformMatrix4fv(self.ViewMatrixLoc, 1, True, self.view_matrix.get_matrix())
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, self.projection_matrix.get_matrix())
        glEnable(GL_DEPTH_TEST)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.mouseRel = Vector(0, 0, 0)

        self.moveForward = False
        self.moveBack = False
        self.moveLeft = False
        self.moveRight = False

        self.moveUp = False
        self.moveDown = False

    def update(self):
        delta_time = self.clock.tick(60) / 1000.0

        self.view_matrix.add_yaw((self.mouseRel.x * delta_time) / pi)
        self.view_matrix.add_pitch((-self.mouseRel.y * delta_time) / pi)

        if self.moveForward:
            self.view_matrix.move(0, 0, -2 * delta_time)
        if self.moveBack:
            self.view_matrix.move(0, 0, 2 * delta_time)
        if self.moveLeft:
            self.view_matrix.slide(2 * delta_time, 0, 0)
        if self.moveRight:
            self.view_matrix.slide(-2 * delta_time, 0, 0)

        if self.moveUp:
            self.view_matrix.slide(0, 2 * delta_time, 0)
        if self.moveDown:
            self.view_matrix.slide(0, -2 * delta_time, 0)

        glUniformMatrix4fv(self.ViewMatrixLoc, 1, True, self.view_matrix.get_matrix())


    def display(self):

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)


        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
                    if event.key == K_w:
                        self.moveForward = True
                    if event.key == K_s:
                        self.moveBack = True
                    if event.key == K_a:
                        self.moveLeft = True
                    if event.key == K_d:
                        self.moveRight = True
                    if event.key == K_SPACE:
                        self.moveUp = True
                    if event.key == K_LSHIFT:
                        self.moveDown = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
                        self.moveForward = False
                    if event.key == K_s:
                        self.moveBack = False
                    if event.key == K_a:
                        self.moveLeft = False
                    if event.key == K_d:
                        self.moveRight = False
                    if event.key == K_SPACE:
                        self.moveUp = False
                    if event.key == K_LSHIFT:
                        self.moveDown = False

            if pygame.mouse.get_focused():
                v = pygame.mouse.get_rel()
                self.mouseRel = Vector(v[0], v[1], 0)
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()