import struct
import typing
from dataclasses import dataclass
import utils

@dataclass
class Drawable:
    ver: int
    showing: bool
    draw_ct: int
    draws: list[str]

    def __init__(self, file):
        self.ver = struct.unpack("<I", file.read(4))
        self.showing = struct.unpack("<B", file.read(1))
        self.draw_ct = struct.unpack("<I", file.read(4))
        self.draws = [readUntilNull(file) for i in range(draw_ct)]