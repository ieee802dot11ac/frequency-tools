import struct
import typing
from dataclasses import dataclass

@dataclass
class ArkFileEntry:
	file_name_hash: int
	file_name_off: int
	folder_name_idx: int
	block_off: int
	block: int
	file_size: int
	inflated_size: int
	fake_file_address: int
	fake_filename: str
	data: bytes

	def __init__(self):
		self.file_name_hash = 0
		self.file_name_off = 0
		self.folder_name_idx = 0
		self.block_off = 0
		self.block = 0
		self.file_size = 0
		self.inflated_size = 0
		self.fake_file_address = 0
		self.fake_filename = ""
		self.data = b''

	def read(self, file):
		self.file_name_hash = struct.unpack("<I", file.read(4))[0]
		self.file_name_off = struct.unpack("<I", file.read(4))[0]
		self.folder_name_idx = struct.unpack("<H", file.read(2))[0]
		self.block_off = struct.unpack("<H", file.read(2))[0]
		self.block = struct.unpack("<I", file.read(4))[0]
		self.file_size = struct.unpack("<I", file.read(4))[0]
		self.inflated_size = struct.unpack("<I", file.read(4))[0]

	def get_data(self, file, blocksize):
		self.fake_file_address = self.block * blocksize + self.block_off
		file.seek(self.fake_file_address)
		self.data = file.read(self.file_size)

	# TODO impl write

@dataclass
class ArkFolderEntry:
	folder_name_hash: int
	folder_name_off: int
	fake_folder_str: str

	def __init__(self):
		self.folder_name_hash = 0
		self.folder_name_off = 0
		self.fake_folder_str = ""

	def read(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils
		self.folder_name_hash = struct.unpack("<I", file.read(4))[0]
		self.folder_name_off = struct.unpack("<I", file.read(4))[0]
		pos = file.tell()
		file.seek(self.folder_name_off)
		self.fake_folder_str = utils.readUntilNull(file)
		file.seek(pos)

	def write(self, file):
		file.write(struct.pack("<2I", self.folder_name_hash, self.folder_name_off))

@dataclass
class ArkFile:
	magic: int
	version: int
	file_entry_off: int
	file_entry_ct: int
	folder_entry_off: int
	folder_entry_ct: int
	string_table_off: int
	string_ct: int
	total_hdr_size: int
	block_size: int
	file_entries: list[ArkFileEntry]
	folder_entries: list[ArkFolderEntry]
	string_table: list[str]

	def __init__(self):
		self.magic = 0x004B5241 # ARK\0
		self.version = 2
		self.file_entry_off = 0x100
		self.file_entry_ct = 0
		self.folder_entry_off = 0x100
		self.folder_entry_ct = 0
		self.string_table_off = 0x100
		self.string_ct = 0
		self.total_hdr_size = 0x100
		self.block_size = 2048
		self.file_entries = []
		self.folder_entries = []
		self.string_table = []

	def read(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils
		
		self.magic = struct.unpack("<I", file.read(4))[0]
		print(f"MAGIC == {"0x%0.2X" % self.magic}")
		print( "SHOULD = 0x4B5241")
		self.version = struct.unpack("<I", file.read(4))[0]
		self.file_entry_off = struct.unpack("<I", file.read(4))[0]
		self.file_entry_ct = struct.unpack("<I", file.read(4))[0]
		self.folder_entry_off = struct.unpack("<I", file.read(4))[0]
		self.folder_entry_ct = struct.unpack("<I", file.read(4))[0]
		self.string_table_off = struct.unpack("<I", file.read(4))[0]
		self.string_ct = struct.unpack("<I", file.read(4))[0]
		self.total_hdr_size = struct.unpack("<I", file.read(4))[0]
		self.block_size = struct.unpack("<I", file.read(4))[0]
		file.seek(self.file_entry_off)
		self.file_entries = [ArkFileEntry() for _ in range(self.file_entry_ct)]

		for entry in self.file_entries:
			entry.read(file)

		for entry in self.file_entries:
			file.seek(entry.file_name_off)
			entry.fake_filename = utils.readUntilNull(file)
			entry.get_data(file, self.block_size)

		file.seek(self.folder_entry_off)
		self.folder_entries = [ArkFolderEntry() for _ in range(self.folder_entry_ct)]

		for entry in self.folder_entries:
			entry.read(file)

		file.seek(self.string_table_off)
		self.string_table = [utils.readUntilNull(file) for i in range(self.string_ct)]
