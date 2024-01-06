import os # nonlocal imports
import struct
import typing
from dataclasses import dataclass # "from _" imports
from class_defs import common_types as ct # local imports
from class_defs import drawable as dr
from class_defs import transform as tf
from class_defs import utils as ut

@dataclass
class Face:
	idx0: int
	idx1: int
	idx2: int

	def __init__(self, file):
		self.idx0, self.idx1, self.idx2 = struct.unpack("<hhh", file.read(6))

@dataclass
class Vertex:
	# Coordinates
	x: float
	y: float
	z: float
	# Normals
	nx: float
	ny: float
	nz: float
	# UVs
	u: float
	v: float
	# Weights
	weight_0: float
	weight_1: float
	weight_2: float
	weight_3: float
	# Bone indices
	bone_0: int # short
	bone_1: int # short
	bone_2: int # short
	bone_3: int # short

	def __init__(self, file):
		test = file.read(12)
		self.x, self.y, self.z = struct.unpack("<3f", test)
		if abs(self.x) > 0 and abs(self.x) < 0.00001: # hopefully avoid weird errors with absurd precision
			self.x = 0
		if abs(self.y) > 0 and abs(self.y) < 0.00001:
			self.y = 0
		if abs(self.z) > 0 and abs(self.z) < 0.00001:
			self.z = 0
		test = file.read(12)
		self.nx, self.ny, self.nz = struct.unpack("<3f", test)
		if abs(self.nx) > 0 and abs(self.nx) < 0.00001:
			self.nx = 0
		if abs(self.ny) > 0 and abs(self.ny) < 0.00001:
			self.ny = 0
		if abs(self.nz) > 0 and abs(self.nz) < 0.00001:
			self.nz = 0
		test = file.read(8)
		self.u, self.v = struct.unpack("<2f", test)
		if abs(self.u) > 0 and abs(self.u) < 0.00001:
			self.u = 0
		if abs(self.v) > 0 and abs(self.v) < 0.00001:
			self.v = 0
		test = file.read(16)
		self.weight_0, self.weight_1, self.weight_2, self.weight_3 = struct.unpack("<4f", test)
		if abs(self.weight_0) > 0 and abs(self.weight_0) < 0.00001:
			self.weight_0 = 0
		if abs(self.weight_1) > 0 and abs(self.weight_1) < 0.00001:
			self.weight_1 = 0
		if abs(self.weight_2) > 0 and abs(self.weight_2) < 0.00001:
			self.weight_2 = 0
		if abs(self.weight_3) > 0 and abs(self.weight_3) < 0.00001:
			self.weight_3 = 0
		test = file.read(8)
		print(test, file.tell())
		self.bone_0, self.bone_1, self.bone_2, self.bone_3 = struct.unpack("<4h", test)

	@property
	def pos(self):
		return (self.x, self.y, self.z)

	@property
	def norm(self):
		return (self.nx, self.ny, self.nz)

	@property
	def tex(self):
		return (self.u, self.v)

	@property
	def weights(self):
		return (self.weight_0, self.weight_1, self.weight_2, self.weight_3)

	@property
	def bones(self):
		return (self.bone_0, self.bone_1, self.bone_2, self.bone_3)

#struct FreqMesh {
#	u32 version;
#	Transform tfm;
#	Drawable draw;
#	padding[4];
#	u32 bone_ct;
#	strwrap bones[bone_ct];
#	u32 zmode1;
#	u32 zmode2;
#	char mat[];
#	char owner[];
#	char alt_geom_owner[];
#	char trans_parent[];
#	char trans_1[];
#	char trans_2[];
#	float sphere[4];
#	char huh2[];
#	float huh3;
#	u32 ohno;
#	u32 vert_ct;
#	Vertex verts[vert_ct];
#	u32 face_ct;
#	Face faces[face_ct];
#	u32 short_ct;
#	u16 shorts[short_ct*2];
#};

@dataclass
class RndMesh:
	ver: int
	xfm: tf.Transform # RndTransformable
	draw: dr.Drawable # RndDrawable
	bone_ct: int
	bones: list[str]
	zmode1: int
	zmode2: int
	mat: str
	owner: str
	owner2: str
	parent: str
	trans1: str
	trans2: str
	sphere: ct.Sphere
	unk_str: str
	unk_flt: float
	unk_negone: int
	vert_ct: int
	verts: list[Vertex]
	face_ct: int
	faces: list[Face]
	short_ct: int
	shorts: list[int] # 2 * short_ct... why?

	def __init__(self, file):
		self.ver = struct.unpack("<I", file.read(4))
		self.xfm = tf.Transform(file)
		self.draw = dr.Drawable(file)
		file.seek(4,1)
		self.bone_ct = struct.unpack("<I", file.read(4))[0]
		self.bones = [ut.readUntilNull(file) for i in range(self.bone_ct)]
		self.zmode1 = struct.unpack("<I", file.read(4))
		self.zmode2 = struct.unpack("<I", file.read(4))
		self.mat = ut.readUntilNull(file)
		self.owner = ut.readUntilNull(file)
		self.owner2 = ut.readUntilNull(file)
		self.parent = ut.readUntilNull(file)
		self.trans1 = ut.readUntilNull(file)
		self.trans2 = ut.readUntilNull(file)
		self.sphere = ct.Sphere(file)
		self.unk_str = ut.readUntilNull(file)
		self.unk_flt = struct.unpack("<f", file.read(4))[0]
		self.unk_negone = struct.unpack("<I", file.read(4))
		self.vert_ct = struct.unpack("<I", file.read(4))[0]
		self.verts = [Vertex(file) for j in range(self.vert_ct)]
		self.face_ct = struct.unpack("<I", file.read(4))[0]
		self.faces = [Face(file) for k in range(self.face_ct)]
		self.short_ct = struct.unpack("<I", file.read(4))[0]
		self.shorts = [struct.unpack("<h", file.read(2)) for l in range(2*self.short_ct)]
