from .build.huff_build import HuffBuild
from .algorithms.huffman import HuffmanCoding
from .algorithms.lzw import LZWCoding
from pathlib import Path
import unittest
from .base.enums import CodingType
from .tests.huffman_test import TestHuffmanCoding
from .tests.lzw_test import TestLZW
from typer import Typer, Argument, Option
from rich.console import Console
import os
import sys
import io

app = Typer()
console = Console()


@app.command(name='huff')
def execute_file(file: Path = Argument(..., exists=True),
                 output: Path = Option('./', '-o', '--out-path', dir_okay=True,
                                       help='Path to directory, works only with .huff files'),
                 algorithm: CodingType = Option(CodingType.HUFFMAN, '-a', '--algorithm',
                                                help='Compress or decompress file with huffman or lzw algorithm')
                 ):
	match algorithm, file.suffix:
		case _, '.lzw':
			algorithm = LZWCoding
		case _, '.huff':
			algorithm = HuffmanCoding
		case CodingType.HUFFMAN, _:
			algorithm = HuffmanCoding
		case CodingType.LZW, _:
			algorithm = LZWCoding

		case _:
			raise Exception('Wrong algorithm')

	build = HuffBuild(directory=output, file=file, algorithm=algorithm)
	fn = build.execute_func()
	if fn == build.execute_compression:
		with console.status("[bold green]Compressing...", spinner="growHorizontal"):
			res = build.execute(func=fn)

	else:
		with console.status("[bold green]Decompressing...", spinner="growHorizontal"):
			res = build.execute(func=fn)

	console.print(res)


if __name__ == "__main__":
	tests = unittest.TestLoader().discover('tests', pattern='*.py')
	suite = unittest.TestSuite(tests)
	with open(os.devnull, 'w') as f:
		pass
	result = unittest.TextTestRunner(stream=f, verbosity=2).run(suite)
	if result.wasSuccessful():
		app()
	else:
		raise SystemExit
