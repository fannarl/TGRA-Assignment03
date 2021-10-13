
import pygame
from pygame.locals import *
from pygame.math import *

from math import *
from Base3DObjects import *

from maze import *

#2D test for which side of a 2D line a 2D point lies on
def leftOf(a, b, p):
    # 3x3 determinant (can also think of this aprojecting onto 2D lines)
    # | ax  bx  px |
    # | ay  by  py |
    # | 1   1   1  |
  
    area = 0.5 * (a.x * (b.y - p.y) +
                  b.x * (p.y - a.y) +
                  p.x * (a.y - b.y))
    return (area > 0.0)

def project2D(planeX, planeY, v):
    return Vector2(v.dot(planeX), v.dot(planeY))

def fancyCollisionCheck(scene, pos):
    collisionRadius = 0.1
    collisionCounter = 0

    shiftDelta = Vector3()
    numCollisions = 0

    for collider in scene.colliders:
        

        verts = collider.verts
        inds = collider.inds
        normals = collider.normals

        for i in range(0, inds, 3):

            # Get poly to test against
            poly = [ inds[i], inds[i+1], inds[i+2] ]
            v1 = Vector3(verts[poly[0]*3], verts[poly[0]*3 +1], verts[poly[0]*3 +2])
            v2 = Vector3(verts[poly[1]*3], verts[poly[1]*3 +1], verts[poly[1]*3 +2])
            v3 = Vector3(verts[poly[2]*3], verts[poly[2]*3 +1], verts[poly[2]*3 +2])
            n = Vector3(normals[i], normals[i+1], normals[i+2])
            
            # Check plane
            d = -((v1 + v2 + v3) / 3.0).dot(n)
            dtp = n.dot(pos) + d # distance to plane

            if abs(dtp) > collisionRadius:
                continue # no collision, too far away

            # now check if in plane bounderies

            a = v2 - v1
            b = v3 - v2
            c = v1 - v3

            planeX = a.normalized()
            planeY = n.cross(a).normalized()

            planePos2D = project2D(planeX, planeY, pos)
            poly_2D = [ project2D(planeX, planeY, v1), project2D(planeX, planeY, v2), project2D(planeX, planeY, v3) ]

            flag = True
            for i in range(3):
                n = ++i
                if n == 3: n = 0
                
                if not leftOf(poly_2D[i], poly_2D[n], planePos2D):
                    flag = False
                    break 

            if not flag: 
                continue # no collision, not in plane bunderies

            shiftDelta += n * ( collisionRadius - dtp )
            ++numCollisions

def collisionCheck(colliders, pos):
    pass
