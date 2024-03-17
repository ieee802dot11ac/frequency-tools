def import_dingus(f, fname):

    import bpy
    from . class_defs import mesh

    bmesh = bpy.data.meshes.new(fname)
    fmesh = mesh.RndMesh(f)

    bmesh.from_pydata([x.pos for x in fmesh.verts], [], [f.as_tup for f in fmesh.faces])

    bmesh.validate()

    obj = bpy.data.objects.new(fname, bmesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

