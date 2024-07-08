import struct
import typing
from dataclasses import dataclass

@dataclass
class Sphere:
	x: float
	y: float
	z: float
	r: float

	def __init__(self):
		self.x = self.y = self.z = self.r = 0

	def read(self, file):
		self.x, self.y, self.z, self.r = struct.unpack("<4f", file.read(16))

	def write(self, file):
		file.write(struct.pack("<4f", self.x, self.y, self.z, self.r))

@dataclass
class Color4f:
	r: float
	g: float
	b: float
	a: float

	def __init__(self):
		pass

	def read(self, file):
		self.r, self.g, self.b, self.a = struct.unpack("<4f", file.read(16))

	def write(self, file):
		file.write(struct.pack("<4f", self.r, self.g, self.b, self.a))


@dataclass
class Rect:
	x: float
	y: float
	w: float
	h: float

	def __init__(self):
		pass

	def read(self, file):
		self.x, self.y, self.w, self.h = struct.unpack("<4f", file.read(16))


@dataclass
class Vector2:
	x: float
	y: float

	def __init__(self):
		pass

	def read(self, file):
		self.x, self.y = struct.unpack("<2f", file.read(8))

	def write(self, file):
		file.write(struct.pack("<2f", self.x, self.y))

@dataclass
class Vector3:
	x: float
	y: float
	z: float

	def __init__(self):
		self.x = self.y = self.z = 0

	def read(self, file):
		self.x, self.y, self.z = struct.unpack("<3f", file.read(12))

	def write(self, file):
		file.write(struct.pack("<3f", self.x, self.y, self.z))

	@property
	def as_tup(self):
		return [self.x, self.y, self.z]

	def __repr__(self):
		return f"\n[ {self.x} {self.y} {self.z} ]"


@dataclass
class Matrix3:
	row1: Vector3
	row2: Vector3
	row3: Vector3

	def __init__(self):
		self.row1 = Vector3()
		self.row2 = Vector3()
		self.row3 = Vector3()
		self.row1.x = self.row2.y = self.row3.z = 1


	def read(self, file):
		self.row1.read(file)
		self.row2.read(file)
		self.row3.read(file)

	def write(self, file):
		self.row1.write(file)
		self.row2.write(file)
		self.row3.write(file)

	@property
	def as_dbl_tup(self):
		return [self.row1.as_tup, self.row2.as_tup, self.row3.as_tup]

	def __repr__(self):
		return f"{self.row1}{self.row2}{self.row3}"

@dataclass
class Xfm:
	rot: Matrix3
	pos: Vector3
	
	def __init__(self):
		self.rot = Matrix3()
		self.pos = Vector3()

	def read(self, file):
		self.rot.read(file)
		self.pos.read(file)

	def write(self, file):
		self.rot.write(file)
		self.pos.write(file)
