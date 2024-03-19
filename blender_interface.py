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

    flit = light.Light(f)
    typ = ''
    if flit.mType == 0:
        typ = 'POINT'
    elif flit.mType == 1:
        typ = 'AREA'
    elif flit.mType == 2:
        typ = 'SPOT'
    blit = bpy.data.lights.new(name=fname, type=typ)
    blit.energy = flit.diffuse.a

    blit_obj = bpy.data.objects.new(name=fname, object_data = blit)
    bpy.context.scene.collection.objects.link(blit_obj)
    bpy.context.view_layer.objects.active = blit_obj
    blit_obj.location = flit.tform.pos
    bpy.context.evaluated_depsgraph_get().update()

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

