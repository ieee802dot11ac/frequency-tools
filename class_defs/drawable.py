import struct
import typing
from dataclasses import dataclass

@dataclass
class Drawable:
	ver: int
	showing: bool
	draw_ct: int
	draws: list[str]

	def __init__(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		self.ver = struct.unpack("<I", file.read(4))
		self.showing = struct.unpack("<B", file.read(1))
		self.draw_ct = struct.unpack("<I", file.read(4))[0]
		self.draws = [utils.readUntilNull(file) for i in range(self.draw_ct)]
