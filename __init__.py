bl_info = {
    "name": "FreQuency Mesh importer",
    "author": "ieee 802.11ac",
    "version": (1, 0, 0),
    "blender": (2, 81, 6),
    "location": "File > Import",
    "description": "Import FreQuency meshes",
    "category": "Import",
}

import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)

from bpy_extras.io_utils import ImportHelper

from bpy.types import (
    Operator,
    OperatorFileListElement,
)

class ImportFrqMesh(Operator, ImportHelper):
    bl_idname = "import_mesh.freq"
    bl_label = "Import FreQuency mesh"
    bl_description = "Load FreQuency triangle mesh data"
    bl_options = {'UNDO'}

    filename_ext = ".stl"

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )

    directory: StringProperty(
        subtype='DIR_PATH',
    )

    def execute(self, context):
        import os
        from . blender_interface import import_dingus

        paths = [os.path.join(self.directory, name.name) for name in self.files]
        for path in paths:
            objName = bpy.path.display_name_from_filepath(path)
            f = open(path, "rb")
            import_dingus(f, objName)

        return {'FINISHED'}

    def draw(self, context):
        pass


def menu_import(self, context):
    self.layout.operator(ImportFrqMesh.bl_idname, text="FreQuency mesh (.mesh)")

def register():
    bpy.utils.register_class(ImportFrqMesh)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)

def unregister():
    bpy.utils.unregister_class(ImportFrqMesh)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
