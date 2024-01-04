#!/usr/bin/python3

import gzip as gz
import os
import struct
import sys
import tempfile as tf
import typing
from dataclasses import dataclass

def readUntilNull(file) -> str:
	ret = b""
	c = b' '
	while True:
		c = bytes(file.read(1))
		if c == b'\0':
			break
		ret += c
	return str(ret)[2:-1]

@dataclass
class RndEntry:
	ftype: str
	fname: str
	unk_bool: bool

	def Load(self, file):
		self.ftype = readUntilNull(file)
		self.fname = readUntilNull(file)
		self.unk_bool = file.read(1)
		print("new file of type", self.ftype, "named", self.fname, "with unk_bool of", self.unk_bool)

if len(sys.argv) == 1:
	print("i can't unpack nothing")
	exit()


if len(sys.argv) == 3:
	print("Dumping file", sys.argv[1], "to directory", sys.argv[2])

if '.gz' in sys.argv[1]:
	filename = sys.argv[1][:-3]
	gzFile = gz.open(sys.argv[1])
	file = tf.TemporaryFile()
	file.write(gzFile.read())
	file.seek(0, 0)
else:
	filename = sys.argv[1]
	file = open(filename, "rb")

if len(sys.argv) == 2:
	print("Dumping file", sys.argv[1], 'to _' + filename[:-4])

ver: int = struct.unpack_from("<I", file.read(4))[0]
entryCt: int = struct.unpack_from("<I", file.read(4))[0]
entries = [RndEntry("", "", 0) for h in range(entryCt)]

for entry in entries:
	entry.Load(file)

remainder = file.read()
files = remainder.split(b"\xAD\xDE\xAD\xDE")

print("file ver:", ver, "\nfile entries:", entryCt, "\nrest of file length:", len(remainder))

if len(sys.argv) == 3 and os.path.exists(sys.argv[2]):
	os.chdir(sys.argv[2])

if len(sys.argv) == 2 and not os.path.exists(filename[:-4]):
	try:
		 os.mkdir("_" + filename[:-4])
		 os.chdir("_" + filename[:-4])
	except:
		os.chdir("_" + filename[:-4])

if len(entries) != len(files) - 1:
	print("SUPER BAD ERROR!!! CHUNK COUNT DOES NOT MATCH ENTRY COUNT!!!")
	print("entries length:", len(entries), "files length:", len(files))
	exit()

for i in range(entryCt):
	name = ""
	if ('.' in entries[i].fname):
		name = entries[i].fname
	else:
		name = entries[i].fname + "." + entries[i].ftype.lower()
	outFile = open(name, "wb")
	outFile.write(files[i])
