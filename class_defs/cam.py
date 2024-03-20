import typing
import struct
from dataclasses import dataclass
from .. class_defs import common_types as ct
from .. class_defs import transform as tf
from .. class_defs import drawable as dr
from .. class_defs import collideable as cl

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
    target_tex: str
    # y_ratio: float # breaks if target_tex

    def __init__(self, file):

        from .. class_defs import utils as ut

        self.ver = struct.unpack("<I", file.read(4))[0]
        self.trans = tf.Transform(file)
        self.draw = dr.Drawable(file)
        self.collid = cl.Collideable(file)
        self.near_plane, self.far_plane, self.fov = struct.unpack("<3f", file.read(12))
        self.screen_rect = ct.Rect(file)
        self.z_range = ct.Vector2(file)
        self.target_tex = ut.readUntilNull(file)
        # self.y_ratio = struct.unpack("<f", file.read(4))[0]

