import typing
import struct
from dataclasses import dataclass
try:
    from .. class_defs import common_types as ct
    from .. class_defs import transform as tf
    from .. class_defs import drawable as dr
    from .. class_defs import collideable as cl
except:
    from class_defs import common_types as ct
    from class_defs import transform as tf
    from class_defs import drawable as dr
    from class_defs import collideable as cl

@dataclass
class Cam:
    ver: int # 8
    trans: tf.Transform
    draw: dr.Drawable
    collid: cl.Collideable
    near_plane: float
    far_plane: float
    fov: float
    screen_rect: ct.Rect
    z_range: ct.Vector2
    target_tex_exists: bool 
    target_tex: str
    y_ratio: float

    def __init__(self):
        self.ver = 8
        self.trans = tf.Transform()
        self.draw = dr.Drawable()
        self.collid = cl.Collideable()
        self.screen_rect = ct.Rect()
        self.z_range = ct.Vector2()

    def read(self, file):
        try:
            from .. class_defs import utils as ut
        except:
            from class_defs import utils as ut

        self.ver = struct.unpack("<I", file.read(4))[0]
        self.trans.read(file)
        self.draw.read(file)
        self.collid.read(file)
        self.near_plane, self.far_plane, self.fov = struct.unpack("<3f", file.read(12))
        self.screen_rect.read(file)
        self.z_range.read(file)
        self.target_tex_exists = struct.unpack("<B", file.read(1))[0]
        if self.target_tex_exists:
            self.target_tex = ut.readUntilNull(file)
        else:
            self.target_tex = ""
        self.y_ratio = struct.unpack("<f", file.read(4))[0]

