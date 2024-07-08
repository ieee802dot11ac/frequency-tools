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
		self.ver = 5
		self.local = ct.Xfm()
		self.world = ct.Xfm()
		self.trans_ct = 0
		self.transes = []
		self.billboard = 0
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
		return self.world.pos.as_tup()

	def write(self, file):
		file.write(struct.pack("<I", self.ver))
		self.local.write(file)
		self.world.write(file)
		file.write(struct.pack("<I", self.trans_ct))
		[utils.writeCstr(file, s) for s in self.transes]
		file.write(struct.pack("<I", self.billboard))
		self.origin.write(file)

