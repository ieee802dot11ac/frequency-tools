#!/usr/bin/python3
import os
import sys
from class_defs import ark
from class_defs import utils

def print_help():
	print("please provide an archive! if using --print, make sure it's first!")
	exit()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print_help()

	
	if sys.argv[1] == "--print":

		archive = ark.ArkFile()
		file = open(sys.argv[2], "rb")
		archive.read(file)

		print(f"There are {len(archive.file_entries)} files in this archive, and {len(archive.folder_entries)} folders.")
		print(f"The archive itself reports {archive.file_entry_ct} and {archive.folder_entry_ct} entries, respectively.")
		print(f"Folders:")
		for i in range(len(archive.folder_entries)):
			entry = archive.folder_entries[i]
			file.seek(entry.folder_name_off)
			if entry.fake_folder_str == '':
				print(f"\tFolder {i}: Hash {entry.folder_name_hash}, name offset: {entry.folder_name_off}. This is the root folder.")
			else:
				print(f"\tFolder {i}: Hash {entry.folder_name_hash}, name offset: {entry.folder_name_off}, name: {entry.fake_folder_str}")

		print("Files:")
		for i in range(len(archive.file_entries)):
			entry = archive.file_entries[i]
			file.seek(entry.file_name_off)
			name = utils.readUntilNull(file)
			print(f"\tFile {i}: Hash: {entry.file_name_hash}, filename offset: {entry.file_name_off}, folder name index: {entry.folder_name_idx}, in-block offset: {entry.block_off},")
			print(f"\tblock #: {entry.block}, file size: {entry.file_size}, file size (after deflation): {entry.inflated_size}, data address: {entry.fake_file_address}")
			print(f"\tReal filename: {archive.folder_entries[entry.folder_name_idx].fake_folder_str}/{name}\n")

	elif ".ark" in sys.argv[1].lower() and sys.argv[2] != "--print":
		archive = ark.ArkFile()
		file = open(sys.argv[1], "rb")
		archive.read(file)

		root_folder = sys.argv[2]
		os.makedirs(root_folder, exist_ok=True)
		for entry in archive.folder_entries:
			os.makedirs(f"{root_folder}/{entry.fake_folder_str}", exist_ok=True	) if entry.fake_folder_str != "" else None

		for entry in archive.file_entries:
			print(entry.fake_filename)
			output = open(f"{root_folder}/{archive.folder_entries[entry.folder_name_idx].fake_folder_str}/{entry.fake_filename}", "wb")
			output.write(entry.data)

	else:
		print_help()
