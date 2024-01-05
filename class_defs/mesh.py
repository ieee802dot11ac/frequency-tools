import os # nonlocal imports
import struct
import typing
from dataclasses import dataclass # from x imports
import common_types as ct # local imports
import drawable as dr
import transform as tf
import utils as ut

@dataclass
class Face:
	idx0: int
	idx1: int
	idx2: int

	def __init__(self):
		self.idx0 = 0
		self.idx1 = 0
		self.idx2 = 0

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
		x, y, z = struct.unpack("<3f", file.read(12))
		nx, ny, nz = struct.unpack("<3f", file.read(12))
		u, v = struct.unpack("<2f", file.read(8))
		weight_0, weight_1, weight_2, weight_3 = struct.unpack("<4f", file.read(16))
		bone_0, bone_1, bone_2, bone_3 = struct.unpack("<4I", file.read(16))

	def __init__(self):
		# Coordinates
		x = 0
		y = 0
		z = 0
		# Normals
		nx = 0
		ny = 0
		nz = 0
		# UVs
		u = 0
		v = 0
		# Weights
		weight_0 = 0
		weight_1 = 0
		weight_2 = 0
		weight_3 = 0
		# Bone indices
		bone_0 = 0
		bone_1 = 0
		bone_2 = 0
		bone_3 = 0

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
		self.bone_ct = struct.unpack("<I", file.read(4))
		self.bones = [ut.readUntilNull(file) for i in range(bone_ct)]
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
		self.unk_flt = struct.unpack("<f", file.read(4))
		self.unk_negone = struct.unpack("<I", file.read(4))
		self.vert_ct = struct.unpack("<I", file.read(4))
		self.verts = [Vertex(file) for j in range(vert_ct)]
		self.face_ct = struct.unpack("<I", file.read(4))
		self.faces = [Face(file) for k in range(face_ct)]
		self.short_ct = struct.unpack("<I", file.read(4))
		self.shorts = [struct.unpack("<h", file.read(2)) for l in range(2*short_ct)]



