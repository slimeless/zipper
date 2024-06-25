from pathlib import Path


def get_size(path: Path):
	total = 0
	if path.is_file():
		return path.stat().st_size
	for file in path.rglob('*'):
		if file.is_file():
			total += file.stat().st_size
	return total
