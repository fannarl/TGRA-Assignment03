from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

import pygame
from pygame.locals import *

from Shaders import *
from Matrices import *

class maze:
    grid = [0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,1,1,1,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,1,0,1,1,1,1,
            0,0,0,0,1,0,0,0,0,1,
            0,0,0,0,1,0,1,1,1,1,
            0,0,0,0,1,0,1,0,0,0,
            0,0,0,0,1,1,1,0,0,0]

