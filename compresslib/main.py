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


@app.command()
def compress(
		path: Annotated[Path, Argument(help="The path of the file to be compressed", exists=True)],
		algorithm: Annotated[CodingType, Option(CodingType.HUFFMAN,
		                                        '--algorithm', '-a',
		                                        help="The algorithm to be used for compression")]):
	pass


@app.command()
def decompress(
		path: Annotated[str, Argument(help="The path of the file to be decompressed", exists=True, file_okay=True,
		                              formats=[".lzw", ".huff"])],
		output: Annotated[str, Option(help="The path of the output file", dir_okay=True)]):
	pass


if __name__ == "__main__":
	app()
