import struct
import typing
from dataclasses import dataclass

from .. class_defs import common_types as ct
from .. class_defs import transform as tf

@dataclass
class Light:

    ver: int
    tform: tf.Transform
    diffuse: ct.Color4f
    ambient: ct.Color4f
    specular: ct.Color4f
    inner_angle: float
    outer_angle: float
    mRange: float
    constant_atten: float
    linear_atten: float
    quadratic_atten: float
    mType: int # enum 0 = point 1 = direc 2 = spot

    def __init__(self, file):
        self.ver = struct.unpack("<I", file.read(4))[0]
        self.tform = tf.Transform(file)
        self.diffuse = ct.Color4f(file)
        self.ambient = ct.Color4f(file)
        self.specular = ct.Color4f(file)
        self.inner_angle, self.outer_angle, self.mRange, self.constant_atten, self.linear_atten, self.quadratic_atten = struct.unpack("<6f", file.read(24))
        self.mType = struct.unpack("<I", file.read(4))[0]
