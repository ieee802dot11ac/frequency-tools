import struct
import typing
from dataclasses import dataclass

@dataclass
class Sphere:
	x: float
	y: float
	z: float
	w: float

	def __init__(self, file):
		self.x, self.y, self.z, self.w = struct.unpack("<ffff", file.read(16))

@dataclass
class Color4f:
	r: float
	g: float
	b: float
	a: float

	def __init__(self, file):
		self.r, self.g, self.b, self.a = struct.unpack("<4f", file.read(16))


@dataclass
class Rect:
	x: float
	y: float
	w: float
	h: float

	def __init__(self, file):
		self.x, self.y, self.w, self.h = struct.unpack("<4f", file.read(16))


@dataclass
class Vector2:
	x: float
	y: float
	def __init__(self, file):
		self.x, self.y = struct.unpack("<2f", file.read(8))

@dataclass
class Vector3:
	x: float
	y: float
	z: float
	def __init__(self, file):
		self.x, self.y, self.z = struct.unpack("<fff", file.read(12))

@dataclass
class Matrix3:
	row1: Vector3
	row2: Vector3
	row3: Vector3

	def __init__(self, file):
		self.row1 = Vector3(file)
		self.row2 = Vector3(file)
		self.row3 = Vector3(file)

@dataclass
class Xfm:
	rot: Matrix3
	pos: Vector3

	def __init__(self, file):
		self.rot = Matrix3(file)
		self.pos = Vector3(file)
