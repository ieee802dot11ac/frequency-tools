import struct
import typing
from dataclasses import dataclass
from .. class_defs import utils
from .. class_defs import common_types as ct

@dataclass
class Transform:
    ver: int # 0x0
    local: ct.Xfm # 0x4
    world: ct.Xfm # 0x34
    trans_ct: int # 0x64
    transes: list[str]
    pad1: int
    pad2: int
    pad3: int
    pad4: int

    def __init__(self, file):
        self.ver = struct.unpack("<I", file.read(4))[0]
        self.local = ct.Xfm(file)
        self.world = ct.Xfm(file)
        self.trans_ct = struct.unpack("<I", file.read(4))[0]
        self.transes = [utils.readUntilNull(file) for i in range(self.trans_ct)]
        self.pad1, self.pad2, self.pad3, self.pad4 = struct.unpack("<4I", file.read(16))

    @property
    def pos(self):
        return (self.local.pos.x + self.world.pos.x, self.local.pos.y + self.world.pos.y, self.local.pos.z + self.world.pos.z)
