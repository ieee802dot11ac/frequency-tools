#!/usr/bin/python3
import sys
from class_defs import ark
from class_defs import utils

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("i can't read nothing")
        exit()

    archive = ark.ArkFile()
    file = open(sys.argv[1], "rb")
    archive.read(file)

    print(f"There are {len(archive.file_entries)} files in this archive, and {len(archive.folder_entries)} folders.")
    print(f"The archive itself reports {archive.file_entry_ct} and {archive.folder_entry_ct} entries, respectively.")
    print(f"Folders:")
    for i in range(len(archive.folder_entries)):
        entry = archive.folder_entries[i]
        file.seek(entry.folder_name_off)
        name = utils.readUntilNull(file)
        if (name == ''):
            print(f"\tFolder {i}: Hash {entry.folder_name_hash}, name offset: {entry.folder_name_off}. This is the root folder.")
        else:
            print(f"\tFolder {i}: Hash {entry.folder_name_hash}, name offset: {entry.folder_name_off}, name: {name}")

    print("Files:")
    for i in range(len(archive.file_entries)):
        entry = archive.file_entries[i]
        file.seek(entry.file_name_off)
        name = utils.readUntilNull(file)
        print(f"\tFile {i}: Hash: {entry.file_name_hash}, filename offset: {entry.file_name_off}, folder name index: {entry.folder_name_idx}, in-block offset: {entry.block_off},")
        print(f"\tblock #: {entry.block}, file size: {entry.file_size}, file size (after deflation): {entry.inflated_size}, data address: {entry.real_address}")
        print(f"\tReal filename: {archive.folder_entries[entry.folder_name_idx].fake_folder_str}/{name}\n")
