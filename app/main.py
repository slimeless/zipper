from .build.huff_build import HuffBuild
from .algorithms.lzw import LZWCoding
from .algorithms.huffman import HuffmanCoding
from .base.metric_model import TraceBack
from pathlib import Path
import unittest
from .base.enums import CodingType
from typer import Typer, Argument, Option
from rich.console import Console
import os
import sys

app = Typer()
console = Console()


@app.command(name='huff')
def execute_file(file: Path = Argument(..., exists=True),
                 output: Path = Option('./', '-o', '--out-path', dir_okay=True,
                                       help='Path to directory, works only with .huff files'),
                 algorithm: CodingType = Option(CodingType.HUFFMAN, '-a', '--algorithm',
                                                help='Compress or decompress file with huffman or lzw algorithm')
                 ):
	try:
		raise Exception('Not implemented')
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
				res = build.execute_decompression()

		else:
			with console.status("[bold green]Decompressing...", spinner="growHorizontal"):
				res = build.execute(func=fn)

		console.print(res)

	except Exception as e:
		tb = sys.exc_info()[2]
		traceback = TraceBack(name=type(e).__name__, message=str(e), traceback=tb)
		console.print(traceback)


if __name__ == "__main__":
	app()
