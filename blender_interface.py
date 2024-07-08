def apply_xfmation(blobj, ftrans):
    import mathutils
    import math
    rot_mtx = mathutils.Matrix(ftrans.world.rot.as_dbl_tup)
    # rot_mtx = rot_mtx @ mathutils.Matrix.Rotation(math.pi / 4, 3, "X") # TODO figure out if actually necessary
    mat_loc = mathutils.Matrix.LocRotScale(mathutils.Vector(ftrans.world.pos.as_tup), rot_mtx, None)
    # mat_rot = mathutils.Matrix(ftrans.world.rot.as_dbl_tup)
    # mat_rot.resize_4x4() # else it doesn't work
    # mat_sca = mathutils.Matrix.Scale(1.0, 4, (1.0, 1.0, 1.0)) # Scale set to <1, 1, 1>, can be changed if needed
    blobj.matrix_basis = mat_loc # @ mat_rot @ mat_sca

def import_mesh(f, fname):

    import bpy
    from . class_defs import mesh

    bmesh = bpy.data.meshes.new(fname)
    fmesh = mesh.Mesh()
    fmesh.read(f)

    bmesh.from_pydata([x.pos for x in fmesh.verts], [e.as_tup for e in fmesh.edges], [f.as_tup for f in fmesh.faces])

    bmesh.validate()

    obj = bpy.data.objects.new(fname, bmesh)
    apply_xfmation(obj, fmesh.xfm)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

def export_mesh(f, obj):

    import bpy
    from . class_defs import mesh

    bmesh = obj.data # hope you got the mesh selected :)
    fmesh = mesh.Mesh()
    fmesh.xfm.local.pos.x = obj.matrix_local[0][3]
    fmesh.xfm.local.pos.y = obj.matrix_local[1][3]
    fmesh.xfm.local.pos.z = obj.matrix_local[2][3]

    if obj.material_slots and len(obj.material_slots) > 0:
        material = obj.material_slots[0].material
        if material:
            material_name = material.name
        else:
            material_name = ""
    else:
        material_name = ""

    fmesh.mat = material_name
    
    fmesh.max_verts = -1

    fmesh.vert_ct = len(bmesh.vertices)
    fmesh.verts = [mesh.Vertex() for _ in range(fmesh.vert_ct)]
    for i in range(fmesh.vert_ct):
        bv = bmesh.vertices[i]
        fv = fmesh.verts[i]
        fv.x = bv.co.x
        fv.y = bv.co.y
        fv.z = bv.co.z
        fv.nx = bv.normal.x
        fv.ny = bv.normal.y
        fv.nz = bv.normal.z

    bfaces = [p.vertices for p in bmesh.polygons if len(p.vertices) == 3] # thanks comp
    fmesh.face_ct = len(bfaces)
    fmesh.faces = [mesh.Face() for _ in range(fmesh.face_ct)]
    for i in range(fmesh.edge_ct):
        bf = bfaces[i]
        ff = fmesh.faces[i]
        ff.idx0 = bf.vertices[0]
        ff.idx1 = bf.vertices[1]
        ff.idx2 = bf.vertices[2]

    fmesh.edge_ct = len(bmesh.edges)
    fmesh.edges = [mesh.Edge() for _ in range(fmesh.edge_ct)]
    for i in range(fmesh.edge_ct):
        fmesh.edges[i].idx0 = bmesh.edges[i].vertices[0]
        fmesh.edges[i].idx1 = bmesh.edges[i].vertices[1]

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

