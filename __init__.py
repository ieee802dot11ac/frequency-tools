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

from bpy_extras.io_utils import (
    ImportHelper, 
    ExportHelper
)

from bpy.types import (
    Operator,
    OperatorFileListElement,
)

class ImportFreqMesh(Operator, ImportHelper):
    bl_idname = "import_mesh.freq"
    bl_label = "Import FreQuency mesh"
    bl_description = "Load FreQuency triangle mesh data"
    bl_options = {'UNDO'}

    filename_ext = ".mesh"

    filter_glob: StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
    )

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )

    directory: StringProperty(
        subtype='DIR_PATH',
    )

    def execute(self, context):
        import os
        from . import blender_interface as bi

        paths = [os.path.join(self.directory, name.name) for name in self.files]
        for path in paths:
            objName = bpy.path.display_name_from_filepath(path)
            f = open(path, "rb")
            bi.import_mesh(f, objName)

        return {'FINISHED'}

class ImportFreqScene(Operator, ImportHelper):
    bl_idname = "import_scene.freq"
    bl_label = "Import FreQency Rnd scene"
    bl_description = "Import contents of a Rnd scene"
    bl_options = {'UNDO'}

    filename_ext = ".rnd, .rnd.gz"

    filter_glob: StringProperty(
        default="*.rnd*",
        options={'HIDDEN'},
    )

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )

    directory: StringProperty(
        subtype='DIR_PATH',
    )

    def execute(self, context):
        import os
        from . import blender_interface as bi
        from . class_defs import utils

        paths = [os.path.join(self.directory, name.name) for name in self.files]
        for path in paths:
            objName = bpy.path.display_name_from_filepath(path)
            f = utils.OpenOptionallyCompressed(path)
            bi.import_rnd(f, objName)

        return {'FINISHED'}

class ExportFreqMesh(Operator, ExportHelper):
    bl_idname = "export_mesh.freq"
    bl_label = "export FreQuency mesh"
    bl_description = "Write FreQuency mesh (no UVs, bones, or LOD)"
    bl_options = {'UNDO'}

    filename_ext = ".mesh"

    filter_glob: StringProperty(
        default="*.mesh",
        options={'HIDDEN'},
        maxlen=255,
    )

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )

    directory: StringProperty(
        subtype='DIR_PATH',
    )

    def execute(self, context):
        import os
        from . import blender_interface as bi

            
        f = open(self.filepath, "wb")
        bi.export_mesh(f, bpy.context.object)

        return {'FINISHED'}

def menu_import(self, context):
    self.layout.operator(ImportFreqMesh.bl_idname, text="FreQuency mesh (.mesh)")
    self.layout.operator(ImportFreqScene.bl_idname, text="FreQuency Rnd (.rnd, .rnd.gz)")

def menu_export(self, context):
    self.layout.operator(ExportFreqMesh.bl_idname, text="FreQuency mesh (.mesh)")

classes = (
    ImportFreqMesh,
    ImportFreqScene,
    
    ExportFreqMesh,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export)
