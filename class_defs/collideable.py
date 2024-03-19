import struct
import typing
from dataclasses import dataclass

@dataclass
class Collideable:
    ver: int # 0
    collide_ct: int
    collides: list[str]

    def __init__(self, file):

        from .. class_defs import utils

        self.ver = struct.unpack("<I", file.read(4))[0]
        self.collide_ct = struct.unpack("<I", file.read(4))[0]
        self.collides = [utils.readUntilNull(file) for i in range(self.collide_ct)]
