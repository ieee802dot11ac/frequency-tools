import struct
import typing
from dataclasses import dataclass

@dataclass
class Collideable:
	ver: int # 0
	collide_ct: int
	collides: list[str]

	def __init__(self):
		self.ver = 0
		self.collide_ct = 0
		self.collides = []

	def read(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		self.ver = struct.unpack("<I", file.read(4))[0]
		self.collide_ct = struct.unpack("<I", file.read(4))[0]
		self.collides = [utils.readUntilNull(file) for i in range(self.collide_ct)]

	def write(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		file.write(struct.pack("<I", self.ver))
		file.write(struct.pack("<I", self.collide_ct))
		[utils.writeCstr(s, file) for s in self.collides]
