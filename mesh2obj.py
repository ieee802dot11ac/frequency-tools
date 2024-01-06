#!/usr/bin/python3
import sys
from class_defs import utils
from class_defs import mesh

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("i can't convert nothing")
        exit()

    if len(sys.argv) == 2:
        outname = sys.argv[1][:-5] + ".obj"

    if len(sys.argv) >= 3:
        outname = sys.argv[2]

    print("Converting", sys.argv[1], "to", outname)

    infile = open(sys.argv[1], "rb")
    mesh = mesh.RndMesh(infile)
    outfile = open(outname, "wt+")
    outfile.write("# Generated by FrequencyTools\n")
    outfile.write("o " + outname.split("/")[-1][:-4] + "\n")
    for vert in mesh.verts:
        outfile.write("v " + str(vert.x) + " " + str(vert.y) + " " + str(vert.z))
        outfile.write("\n")
        outfile.write("vn " + str(vert.nx) + " " + str(vert.ny) + " " + str(vert.nz))
        outfile.write("\n")
        outfile.write("vt " + str(vert.u) + " " + str(vert.v))
        outfile.write("\n")
        
    
    for face in mesh.faces:
        outfile.write("f " + str(face.idx0) + "/" + str(face.idx0) + "/" + str(face.idx0) + " "\
             + str(face.idx1) + "/" + str(face.idx1) + "/" + str(face.idx1)\
             + " " + str(face.idx2) + "/" + str(face.idx2) + "/" + str(face.idx2))
        outfile.write("\n")