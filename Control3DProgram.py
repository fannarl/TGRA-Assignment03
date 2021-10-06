
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

from maze import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        # hide mouse and grab input
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.grid = [[1,1,1,1,1,1,1,1,1,1],
                     [1,0,0,0,0,0,0,0,0,1],
                     [1,1,1,0,1,1,1,1,0,1],
                     [1,0,1,0,1,0,1,1,0,1],
                     [1,0,1,0,1,0,1,1,0,1],
                     [1,0,1,2,1,0,0,2,0,1],
                     [1,0,1,0,1,1,1,1,0,1],
                     [1,0,1,0,1,0,0,1,0,1],
                     [1,0,0,0,1,0,0,2,0,1],
                     [1,0,1,1,1,1,1,1,1,1],]

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(10, 10, 0), Point(3, 3, 1), Vector(0, 0, 1))

        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.mouseRel = Vector(0, 0, 0)
        self.UP_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.Q_key_down = False
        self.E_key_down = False
        self.move_up = False
        self.move_down = False

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick(60) / 1000.0

        self.view_matrix.yaw(-self.mouseRel.x * 0.001)
        self.view_matrix.pitch(-self.mouseRel.y * 0.001)

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if self.W_key_down:
            self.view_matrix.slide(0, 0, -2 * delta_time)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, 2 * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(2 * delta_time, 0, 0)
        if self.D_key_down:
            self.view_matrix.slide(-2 * delta_time, 0, 0)

        if self.move_up:
            self.view_matrix.slide(0, 2 * delta_time, 0)
        if self.move_down:
            self.view_matrix.slide(0, -2 * delta_time, 0)

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

        for i in range(len(self.grid)):
                for x in range(len(self.grid[i])):
                    if self.grid[i][x] == 1:
                        self.model_matrix.push_matrix()
                        self.model_matrix.add_translation(float(i), float(x), 0.0)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
                        self.model_matrix.add_scale(1.0, 1.0, 3.0)
                        self.shader.set_model_matrix(self.model_matrix.matrix)
                        self.cube.draw(self.shader)
                        self.model_matrix.pop_matrix()
                    elif self.grid[i][x] == 2:
                        self.model_matrix.push_matrix()
                        self.model_matrix.add_translation(float(i), float(x), 0.0)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
                        self.model_matrix.add_rotate_z(self.angle)
                        self.model_matrix.add_scale(0.2, 1.0, 3.0)
                        self.shader.set_model_matrix(self.model_matrix.matrix)
                        self.cube.draw(self.shader)
                        self.model_matrix.pop_matrix()


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
                    if event.key == K_SPACE:
                        self.move_up = True
                    if event.key == K_LSHIFT:
                        self.move_down = True

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
                    if event.key == K_SPACE:
                        self.move_up = False
                    if event.key == K_LSHIFT:
                        self.move_down = False

            if pygame.mouse.get_focused():
                v = pygame.mouse.get_rel()
                self.mouseRel = Vector(v[0], v[1], 0)
                # print(v)
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()