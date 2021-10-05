
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(3, 3, 3), Point(0, 0, 0), Vector(0, 1, 1))

        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.Q_key_down = False
        self.E_key_down = False

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if self.W_key_down:
            self.view_matrix.slide(0, 0, -1 * delta_time)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, 1 * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(-1 * delta_time, 0, 0)
        if self.D_key_down:
            self.view_matrix.slide(1 * delta_time, 0, 0)

        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.1 * delta_time

        if self.Q_key_down:
            self.view_matrix.roll(-pi * delta_time)
        if self.E_key_down:
            self.view_matrix.roll(pi * delta_time)

        if self.UP_key_down:
            self.white_background = True
        else:
            self.white_background = False
    

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.model_matrix.load_identity()

        self.cube.set_vertices(self.shader)

        self.shader.set_solid_color(1.0, 1.0, 0.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3.0, 0.0, 0.0)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        self.model_matrix.add_scale(3.0, 3.0, 3.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.shader.set_solid_color(0.0, 0.0, 1.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 3.0, 0.0)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        self.model_matrix.add_rotate_z(self.angle)
        self.model_matrix.add_scale(0.2, 2.5, 1.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.shader.set_solid_color(1.0, 0.0, 1.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 0.0, -3.0)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        self.model_matrix.add_rotate_x(self.angle * 0.4)
        self.model_matrix.add_rotate_y(self.angle * 0.2453)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        # self.shader.set_solid_color(1.0, 1.0, 0.0)

        # self.model_matrix.push_matrix()
        # self.model_matrix.add_rotate_z(self.angle)

        # self.cube.set_vertices(self.shader)

        # for y in range(10):
        #     for x in range(10):
        #         for z in range(10):
        #             self.shader.set_solid_color(1.0, 0.0, 1.0)
        #             self.model_matrix.push_matrix()
        #             self.model_matrix.add_translation(-5.0 + x, -5.0 + y, 0.0 - z)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        #             self.model_matrix.add_scale(0.8, 0.8, 0.8)
        #             self.shader.set_model_matrix(self.model_matrix.matrix)
        #             self.cube.draw(self.shader)
        #             self.model_matrix.pop_matrix()

        # self.model_matrix.pop_matrix()


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
                        
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_t:
                        self.T_key_down = True
                    if event.key == K_g:
                        self.G_key_down = True
                    if event.key == K_q:
                        self.Q_key_down = True
                    if event.key == K_e:
                        self.E_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_t:
                        self.T_key_down = False
                    if event.key == K_g:
                        self.G_key_down = False
                    if event.key == K_q:
                        self.Q_key_down = False
                    if event.key == K_e:
                        self.E_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()