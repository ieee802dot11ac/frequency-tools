import struct
import typing
from dataclasses import dataclass
try:
	from .. class_defs import utils
	from .. class_defs import common_types as ct
except:
	from class_defs import utils
	from class_defs import common_types as ct

@dataclass
class Transform:
	ver: int # 0x0
	local: ct.Xfm # 0x4
	world: ct.Xfm # 0x34
	trans_ct: int # 0x64
	transes: list[str]
	billboard: int
	origin: ct.Vector3

	def __init__(self):
		self.local = ct.Xfm()
		self.world = ct.Xfm()
		self.origin = ct.Vector3()

	def read(self, file):
		self.ver = struct.unpack("<I", file.read(4))[0]
		self.local.read(file)
		self.world.read(file)
		self.trans_ct = struct.unpack("<I", file.read(4))[0]
		self.transes = [utils.readUntilNull(file) for i in range(self.trans_ct)]
		self.billboard = struct.unpack("<I", file.read(4))[0]
		self.origin.read(file)

	@property
	def pos(self):
		return (self.world.pos.x, self.world.pos.y, self.world.pos.z) 

	def write(self, file):
		file.write(struct.pack("<I"), self.ver)
		self.local.write(file)
		self.world.write(file)
