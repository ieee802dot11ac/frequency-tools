import struct
import typing
from dataclasses import dataclass

@dataclass
class RndEntry:
	ftype: str
	fname: str
	""" looking in Rnd::Manager::LoadObjects, there appears to be some nonsense about merging
	rnd entries, which i *think* is gated behind this bool? i genuinely have zero clue, i'm 
	just always gonna write it as true """
	unk_bool: bool 

	def read(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		self.ftype = utils.readUntilNull(file)
		self.fname = utils.readUntilNull(file)
		self.unk_bool = struct.unpack("B", file.read(1))[0]
		print("new file of type", self.ftype, "named", self.fname, "with unk_bool of", self.unk_bool)

	def write(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		utils.writeCstr(file, self.ftype)
		utils.writeCstr(file, self.fname)
		file.write(struct.pack("<B", self.unk_bool))

@dataclass
class RndFile:
	ver: int
	entryCt: int
	entries: list[RndEntry]
	files: list[bytes]

	def __init__(self):
		self.ver = 6 # note: the 3dsmax plugin we found outputs v5 rnds, TODO figure those out
		self.entryCt = 0
		self.entries = []
		self.files = []

	def LoadRndFile(self, file, diag: bool):
		self.ver = struct.unpack_from("<I", file.read(4))[0]
		self.entryCt = struct.unpack_from("<I", file.read(4))[0]
		self.entries = [RndEntry("", "", 0) for h in range(self.entryCt)]

		for entry in self.entries:
			entry.read(file)

		remainder = file.read()
		self.files = remainder.split(b"\xAD\xDE\xAD\xDE")

		if (diag):
			print("file ver:", self.ver, "\nfile entries:", self.entryCt, "\nrest of file length:", len(remainder))

	def WriteFilesToDir(self, dir: str) -> None:
		import os

		if not os.path.exists(dir):
			os.mkdir(dir)

		os.chdir(dir)

		if len(self.entries) != len(self.files) - 1: # -1 to account for empty entry
			print("SUPER BAD ERROR!!! CHUNK COUNT DOES NOT MATCH ENTRY COUNT!!!")
			print("entries length:", len(self.entries), "\nfiles   length:", len(self.files))
			exit()

		i = 0
		for entry in self.entries:
			name = ""
			if ('.' in entry.fname):
				name = entry.fname
			else:
				name = entry.fname + "." + entry.ftype.lower()
			outFile = open(name, "wb")
			outFile.write(self.files[i])
			i += 1

	def WriteMetadata(self, file): 
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		file.write(struct.pack("<I", self.ver))
		file.write(struct.pack("<I", self.entryCt))

		for entry in self.entries:
			entry.write(file)
		# you can do internal file writing yourself, i don't wanna mess with that