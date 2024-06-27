from .build.huff_build import HuffBuild
from .algorithms.lzw import LZWCoding
from .algorithms.huffman import HuffmanCoding
from .base.metric_model import TraceBack
from pathlib import Path
import unittest
from .base.enums import CodingType
from typer import Typer, Argument, Option, launch
from rich.console import Console
from typer import confirm
from .utils.url import generate_issue_link
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

	except Exception as e:
		tb = sys.exc_info()[2]
		traceback = TraceBack(traceback=tb, info=sys.exc_info())
		console.size = (65, 10)
		console.print(traceback)
		if confirm("Would you like to send issue?", default=False):
			link = generate_issue_link(title=f'[AUTO ISSUE]', body=traceback.info)
			launch(link)


if __name__ == "__main__":
	app()
