import tempfile as tmp
def readUntilNull(file) -> str:
	ret = b""
	c = b' '
	while True:
		c = bytes(file.read(1))
		if c == b'\0':
			break
		ret += c
	return str(ret)[2:-1]

def OpenOptionallyCompressed(name: str):
	if '.gz' in name:
		filename = name[:-3]
		gzFile = gz.open(name)
		file = tmp.TemporaryFile()
		file.write(gzFile.read())
		file.seek(0, 0)
	else:
		filename = name
		file = open(filename, "rb")
	
	return file