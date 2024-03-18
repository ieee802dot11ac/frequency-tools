def import_mesh(f, fname):

    import bpy
    from . class_defs import mesh

    bmesh = bpy.data.meshes.new(fname)
    fmesh = mesh.RndMesh(f)

    bmesh.from_pydata([x.pos for x in fmesh.verts], [], [f.as_tup for f in fmesh.faces])

    bmesh.validate()

    obj = bpy.data.objects.new(fname, bmesh)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def import_light(f, fname):

    import bpy
    from . class_defs import light

    # blit = bpy.data.lights.new()
    flit = light.Light(f)

def import_rnd(f, fname):

    import bpy
    import os
    from . class_defs import rnd
    import tempfile as tf

    masterCollection = bpy.context.scene.collection
    rndCollection = bpy.data.collections.new(fname)
    masterCollection.children.link(rndCollection)

    tempdir = tf.TemporaryDirectory()
    rndFile = rnd.RndFile(0, 0, [rnd.RndEntry("","",False)], [b""])
    rndFile.LoadRndFile(f, False)
    rndFile.WriteFilesToDir(tempdir.name)

    files = os.listdir(tempdir.name)
    for filename in files:
        if ".mesh" in os.path.splitext(filename):
            import_mesh(open(filename, "rb"), filename)
            rndCollection.objects.link(bpy.context.object) #link it with collection
            masterCollection.objects.unlink(bpy.context.object) #unlink it from master collection
        elif ".lit" in os.path.splitext(filename):
            import_light(open(filename, "rb"), filename)
            rndCollection.objects.link(bpy.context.object)
            masterCollection.objects.unlink(bpy.context.object)
        else:
            pass

