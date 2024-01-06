#!/usr/bin/python3
import sys
from class_defs import utils
from class_defs import rnd

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
	rndFile = rnd.RndFile(0, 0, [rnd.RndEntry("","",False)], [b""])
	rndFile.LoadRndFile(file, True)
	rndFile.WriteFilesToDir(outdir)
