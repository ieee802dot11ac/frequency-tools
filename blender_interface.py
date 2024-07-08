def apply_xfmation(blobj, ftrans):
    import mathutils
    mat_loc = mathutils.Matrix.Translation(ftrans.pos)
    # mat_rot = mathutils.Matrix(ftrans.world.rot.as_dbl_tup)
    # mat_rot.resize_4x4() # else it doesn't work
    # mat_sca = mathutils.Matrix.Scale(1.0, 4, (1.0, 1.0, 1.0)) # Scale set to <1, 1, 1>, can be changed if needed
    blobj.matrix_basis = mat_loc # @ mat_rot @ mat_sca

def import_mesh(f, fname):

    import bpy
    from . class_defs import mesh

    bmesh = bpy.data.meshes.new(fname)
    fmesh = mesh.RndMesh()
    fmesh.read(f)

    bmesh.from_pydata([x.pos for x in fmesh.verts], [e.as_tup for e in fmesh.edges], [f.as_tup for f in fmesh.faces])

    bmesh.validate()

    obj = bpy.data.objects.new(fname, bmesh)
    apply_xfmation(obj, fmesh.xfm)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def import_light(f, fname):

    import bpy
    from . class_defs import light

    flit = light.Light()
    flit.read(f)
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
    apply_xfmation(blit_obj, flit.tform)
    bpy.context.evaluated_depsgraph_get().update()

def import_cam(f, fname):

    import bpy
    from . class_defs import cam

    fcam = cam.Cam()
    fcam.read(f)
    bcam_data = bpy.data.cameras.new(fname)
    bcam_data.lens_unit = 'FOV'
    bcam_data.lens = fcam.fov

    bcam = bpy.data.objects.new(name=fname, object_data=bcam_data)
    apply_xfmation(bcam, fcam.trans)

    bpy.context.scene.collection.objects.link(bcam)
    bpy.context.view_layer.objects.active = bcam

def import_rnd(f, fname):

    import bpy
    import os
    from . class_defs import rnd
    import tempfile as tf

    masterCollection = bpy.context.scene.collection
    rndCollection = bpy.data.collections.new(fname)
    masterCollection.children.link(rndCollection)

    tempdir = tf.TemporaryDirectory()
    rndFile = rnd.RndFile()
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
        elif ".cam" in os.path.splitext(filename):
            import_cam(open(filename, "rb"), filename)
            rndCollection.objects.link(bpy.context.object)
            masterCollection.objects.unlink(bpy.context.object)
        else:
            pass

