import struct
import typing
from dataclasses import dataclass

@dataclass
class Sphere: # also used for quaternions
	x: float
	y: float
	z: float
	w: float

	def __init__(self, file):
		x, y, z, w = struct.unpack("<ffff", file.read(16))
	
	def __init__(self, x, y, z, w):
		self.x = x
		self.y = y
		self.z = z
		self.w = w

@dataclass
class Vector3:
	x: float
	y: float
	z: float
	def __init__(self, file):
		x, y, z = struct.unpack("<fff", file.read(12))

	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

@dataclass
class Matrix3:
	row1: Vector3
	row2: Vector3
	row3: Vector3

	def __init__(self, file):
		self.row1 = Vector3(file)
		self.row2 = Vector3(file)
		self.row3 = Vector3(file)
	
	def __init__(self):
		self.row1 = Vector3()
		self.row2 = Vector3()
		self.row3 = Vector3()

@dataclass
class Xfm:
	rot: Matrix3
	pos: Vector3

	def __init__(self, file):
		self.rot = Matrix3(file)
		self.pos = Vector3(file)

	def __init__(self):
		self.rot = Matrix3()
		self.pos = Vector3()