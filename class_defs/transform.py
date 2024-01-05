import struct
import typing
from dataclasses import dataclass
import utils
import common_types as ct

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
        self.ver = struct.unpack("<I", file.read(4))
        self.local = ct.Xfm(file)
        self.world = ct.Xfm(file)
        self.trans_ct = struct.unpack("<I", file.read(4))
        self.transes = [utils.readUntilNull(file) for ignoreme in range(self.trans_ct)]
        self.pad1, self.pad2, self.pad3, self.pad4 = struct.unpack("<4I", file.read(16))

    def __init__(self):
        self.ver = 0
        self.local = ct.Xfm()
        self.world = ct.Xfm()
        self.trans_ct = 0
        self.transes = [""]