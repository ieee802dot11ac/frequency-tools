import struct
import typing
from dataclasses import dataclass

def gen_ark_hash(string: str) -> int:
	stri = bytearray(string, "ascii")
	stri.append(0) # cstr compat
	c: int = int(stri[0])
	i: int = 0
	working1: int = 0
	working2: int = 0
	ret: int = 0
	shift: int = 0
	while c != 0:
		c = int(stri[i]) & 0xFF
		working1 = working2 ^ ((c & 0xFFFF) << shift)
		working2 = working1 & 0xFFFF
		ret = working1
		shift = (shift + 1) & 0x7
		i += 1
	return ret & 0xFFFF


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

	def write(self, file, current_block_count):
		file.write(struct.pack("<IIHH", self.file_name_hash, self.file_name_off, self.folder_name_idx, self.block_off))
		file.write(struct.pack("<III", self.block, self.file_size, self.inflated_size))

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
class ArkStringTableEntry:
	string: str
	fake_file_or_folder_name: bool # true = file
	fake_offset_from_start_of_strtab: int

	def __init__(self):
		self.string = ""
		self.fake_file_or_folder_name = False
		self.fake_offset_from_start_of_strtab = 0

	def __len__(self) -> int:
		return len(self.string) + 1

	def add_string_update_size(self, st: str, size: int) -> int:
		self.string = st
		return self.update_size(size)

	def read(self, file, strtaboff):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils
			
		self.fake_offset_from_start_of_strtab = file.tell() - strtaboff
		self.string = utils.readUntilNull(file)

	def write(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		utils.writeCstr(file, self.string)

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
	string_table: list[ArkStringTableEntry]

	fake_string_table_size: int

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
		self.fake_string_table_size = 0

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
		self.string_table = [ArkStringTableEntry() for i in range(self.string_ct)]

		for entry in self.string_table:
			entry.read(file, self.string_table_off)
			self.fake_string_table_size += len(entry)

	def write(self, file):
		try:
			from .. class_defs import utils
		except:
			from class_defs import utils

		# step 1: generate string table and hashes
		# is this the right way to do it? who knows!
		for entry in self.folder_entries:
			entry.folder_name_hash = gen_ark_hash(entry.fake_folder_str)
			self.string_table.append(entry.fake_folder_str)

		for entry in self.file_entries:
			entry.file_name_hash = gen_ark_hash(entry.fake_filename)
			self.string_table.append(entry.fake_filename)

		# step 2: generate offsets
		self.folder_entry_off = self.file_entry_off + (self.file_entry_ct * 24)
		self.string_table_off = self.folder_entry_off + (self.folder_entry_ct * 8)

		# step 3: write the base header
		file.write(struct.pack("<I", self.magic))
		file.write(struct.pack("<I", self.version))
		file.write(struct.pack("<I", self.file_entry_off))
		file.write(struct.pack("<I", self.file_entry_ct))
		file.write(struct.pack("<I", self.folder_entry_off))
		file.write(struct.pack("<I", self.folder_entry_ct))
		file.write(struct.pack("<I", self.string_table_off))
		file.write(struct.pack("<I", self.string_ct))
		file.write(struct.pack("<I", self.total_hdr_size))
		file.write(struct.pack("<I", self.block_size))

		# step 4: write string table (this makes sense, i promise)
		file.seek(self.string_table_off)
		[utils.writeCstr(file, stri) for stri in self.string_table]
