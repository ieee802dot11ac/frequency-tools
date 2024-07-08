import os # nonlocal imports
import struct
import typing
from dataclasses import dataclass
try:
	from .. class_defs import common_types as ct
	from .. class_defs import collideable as cl
	from .. class_defs import drawable as dr
	from .. class_defs import transform as tf
	from .. class_defs import utils as ut
except:
	from class_defs import common_types as ct
	from class_defs import collideable as cl
	from class_defs import drawable as dr
	from class_defs import transform as tf
	from class_defs import utils as ut

@dataclass
class Face:
	idx0: int
	idx1: int
	idx2: int

	def __init__(self):
		pass

	def read(self, file):
		self.idx0, self.idx1, self.idx2 = struct.unpack("<3h", file.read(6))

	def write(self, file):
		file.write(struct.pack("<3h", self.idx0, self.idx1, self.idx2))

	@property
	def as_tup(self):
		return (self.idx0, self.idx1, self.idx2)

@dataclass
class Edge:
	idx0: int
	idx1: int

	def __init__(self):
		pass

	def read(self, file):
		self.idx0, self.idx1 = struct.unpack("<2h", file.read(4))

	def write(self, file):
		file.write(struct.pack("<2h", self.idx0, self.idx1))

	@property
	def as_tup(self):
		return (self.idx0, self.idx1)

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

	def __init__(self):
		pass

	def read(self, file):
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

		self.bone_0, self.bone_1, self.bone_2, self.bone_3 = struct.unpack("<4h", file.read(8))

	def write(self, file):
		file.write(struct.pack("<3f", self.x, self.y, self.z))
		file.write(struct.pack("<3f", self.nx, self.ny, self.nz))
		file.write(struct.pack("<2f", self.u, self.v))
		file.write(struct.pack("<4f", self.weight_0, self.weight_1, self.weight_2, self.weight_3))
		file.write(struct.pack("<4h", self.bone_0, self.bone_1, self.bone_2, self.bone_3))

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
	coll: cl.Collideable
	zmode1: int
	zmode2: int
	mat: str
	owner: str
	owner2: str
	parent: str
	trans1: str
	trans2: str
	sphere: ct.Sphere
	next_lod: str
	min_screen: float
	max_verts: int
	vert_ct: int
	verts: list[Vertex]
	face_ct: int
	faces: list[Face]
	edge_ct: int
	edges: list[Edge]

	def __init__(self):
		self.xfm = tf.Transform()
		self.draw = dr.Drawable()
		self.coll = cl.Collideable()
		self.sphere = ct.Sphere()

	def read(self, file):
		self.ver = struct.unpack("<I", file.read(4))[0]
		self.xfm.read(file)
		self.draw.read(file)
		self.coll.read(file)
		self.zmode1 = struct.unpack("<I", file.read(4))[0]
		self.zmode2 = struct.unpack("<I", file.read(4))[0]
		self.mat = ut.readUntilNull(file)
		self.owner = ut.readUntilNull(file)
		self.owner2 = ut.readUntilNull(file)
		self.parent = ut.readUntilNull(file)
		self.trans1 = ut.readUntilNull(file)
		self.trans2 = ut.readUntilNull(file)
		self.sphere.read(file)
		self.next_lod = ut.readUntilNull(file)
		self.min_screen = struct.unpack("<f", file.read(4))[0]
		self.max_verts = struct.unpack("<I", file.read(4))[0]
		self.vert_ct = struct.unpack("<I", file.read(4))[0]
		self.verts = [Vertex() for j in range(self.vert_ct)]
		[v.read(file) for v in self.verts]
		self.face_ct = struct.unpack("<I", file.read(4))[0]
		self.faces = [Face() for k in range(self.face_ct)]
		[f.read(file) for f in self.faces]
		self.edge_ct = struct.unpack("<I", file.read(4))[0]
		self.edges = [Edge() for l in range(self.edge_ct)]
		[e.read(file) for e in self.edges]
