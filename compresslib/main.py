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
from typing_extensions import Annotated
import os
import sys

app = Typer()
console = Console()


@app.command('cmp')
def compress(
		path: Path = Argument(help="The path of the file to be compressed", exists=True),
		algorithm: CodingType = Option(CodingType.HUFFMAN,
		                               '--algorithm', '-a',
		                               help="The algorithm to be used for compression")):
	try:
		match algorithm:
			case CodingType.HUFFMAN:
				algo = HuffmanCoding
			case CodingType.LZW:
				algo = LZWCoding
			case _:
				console.print("[red]Invalid algorithm[/red]")
				return

		build = HuffBuild(directory=path.parent, file=path, algorithm=algo)

		fn = build.execute_func()
		with console.status("[bold green]Compressing...", spinner="growHorizontal"):
			res = build.execute(func=fn)
		console.print(res)
	except:
		tb = sys.exc_info()[2]
		traceback = TraceBack(traceback=tb, info=sys.exc_info())
		console.size = (65, 10)
		console.print(traceback)
		if confirm("Would you like to send issue?", default=False):
			link = generate_issue_link(title=f'[AUTO ISSUE]', body=traceback.info)
			launch(link)


@app.command('ucmp')
def decompress(
		path: Path = Argument(help="The path of the file to be decompressed", exists=True, file_okay=True,
		                      formats=[".lzw", ".huff"]),
		output: Path = Option(None, '--output', '-o', help="The path of the output file", dir_okay=True)):
	try:
		match path.suffix:
			case ".lzw":
				algo = LZWCoding
			case ".huff":
				algo = HuffmanCoding
			case _:
				console.print("[red]Invalid algorithm[/red]")
				return

		build = HuffBuild(directory=output or path.parent, file=path, algorithm=algo)
		fn = build.execute_func()
		with console.status("[bold green]Decompressing...", spinner="growHorizontal"):
			res = build.execute(func=fn)
		console.print(res)
	except:
		tb = sys.exc_info()[2]
		traceback = TraceBack(traceback=tb, info=sys.exc_info())
		console.size = (65, 10)
		console.print(traceback)
		if confirm("Would you like to send issue?", default=False):
			link = generate_issue_link(title=f'[AUTO ISSUE]', body=traceback.info)
			launch(link)



if __name__ == "__main__":
	app()
