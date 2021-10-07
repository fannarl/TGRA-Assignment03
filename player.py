
def collisionCheck(scene):
    collisionRadius = 0.1
    collisionCounter = 0

    for item in scene:
        if not item.hasCollision: continue

        verts = item.verts
        normals = item.normals
        tris = item.tries

        for tri in tris:
            # Check plane
            
