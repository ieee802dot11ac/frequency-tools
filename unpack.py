#!/usr/bin/python3
import gzip as gz
import os
import struct
import sys
import typing
from dataclasses import dataclass
from class_defs import utils

@dataclass
class RndEntry:
	ftype: str
	fname: str
	unk_bool: bool

	def Load(self, file):
		self.ftype = utils.readUntilNull(file)
		self.fname = utils.readUntilNull(file)
		self.unk_bool = file.read(1)
		print("new file of type", self.ftype, "named", self.fname, "with unk_bool of", self.unk_bool)

@dataclass
class RndFile:
	ver: int
	entryCt: int
	entries: list[RndEntry]
	files: list[bytes]

	def LoadRndFile(self, file, diag: bool):
		self.ver = struct.unpack_from("<I", file.read(4))[0]
		self.entryCt = struct.unpack_from("<I", file.read(4))[0]
		self.entries = [RndEntry("", "", 0) for h in range(self.entryCt)]

		for entry in self.entries:
			entry.Load(file)

		remainder = file.read()
		self.files = remainder.split(b"\xAD\xDE\xAD\xDE")

		if (diag):
			print("file ver:", self.ver, "\nfile entries:", self.entryCt, "\nrest of file length:", len(remainder))

	def WriteFilesToDir(self, dir: str) -> None:
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
			if ('.' in entry.fname[:-8]): # 8 is a bit large, but it's probably fine
				name = entry.fname
			else:
				name = entry.fname + "." + entry.ftype.lower()
			outFile = open(name, "wb")
			outFile.write(self.files[i])
			i += 1

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("i can't unpack nothing")
		exit()

	if len(sys.argv) == 2:
		if '.gz' in sys.argv[1]:
			filename = sys.argv[1][:-3]
		else:
			filename = sys.argv[1]
		print("Dumping file", sys.argv[1], "to directory _" + filename)
		outdir = "_" + filename[:-4]

	if len(sys.argv) == 3:
		print("Dumping file", sys.argv[1], "to directory", sys.argv[2])
		outdir = sys.argv[2]

	file = utils.OpenOptionallyCompressed(sys.argv[1])
	rnd = RndFile(0, 0, [RndEntry("","",False)], [b""])
	rnd.LoadRndFile(file, True)
	rnd.WriteFilesToDir(outdir)
