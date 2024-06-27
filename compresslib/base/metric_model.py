from pydantic import BaseModel
from rich.panel import Panel
from rich.console import Console, ConsoleOptions
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from typing_extensions import Annotated
from pydantic import BeforeValidator
import traceback
import sys

TracebackLocation = Annotated[
	tuple, BeforeValidator(lambda tb: (x for x in traceback.extract_tb(tb)))]

TracebackInfo = Annotated[
	str, BeforeValidator(lambda info: ''.join(traceback.format_exception(*info)))
]


class TraceBack(BaseModel):
	traceback: TracebackLocation
	info: TracebackInfo

	def __rich_console__(self, console: Console, options: ConsoleOptions):
		exp_type = self._recognize_type_exp()
		layout = Layout(name='root')
		layout.split_row(Layout(name='right'), Layout(name='left'))
		layout['left'].split_column(Layout(name='top'), Layout(name='bottom'))
		layout['right'].update(Panel(Align.center(f'any text', vertical='middle'), style='blue'))
		layout['top'].update(Panel(Align.center(exp_type, vertical='middle'), style='blue', title='Error'))
		layout['bottom'].update(Panel(Align.center('any text', vertical='middle'), style='blue'))
		layout.size = options.size
		yield layout

	def _recognize_type_exp(self):
		is_algorithm = any('algorithms' in x.filename for x in self.traceback)
		if is_algorithm:
			algo = 'huffman' if any('huffman' in x.filename for x in self.traceback) else 'lzw'
			return f'[green]Something went wrong with [bold]{algo}[/bold] algorithm[/green]'
		return f'[green][bold]non[/bold] recognized error[green]'


class FileMetric(BaseModel):
	filename: str
	size: int


class CompressionMetric(BaseModel):
	file: FileMetric
	compressed_file: FileMetric
	ratio: float
	space_saved: float
	elapsed: float

	def __rich_console__(self, console: Console, options: ConsoleOptions):
		yield f'[bold green] Done with compression [magenta]{self.file.filename}[/magenta][/bold green]'
		table = Table(show_header=False, box=None)
		table.add_column('[bold]File', justify='right', no_wrap=True)
		table.add_column('[bold]File', no_wrap=True)
		table.add_row('[bold]Original size', f'[magenta]{self.file.size / 1024 / 1024:.4f}MB')
		table.add_row('[bold]Compressed size', f'[magenta]{self.compressed_file.size / 1024 / 1024:.4f}MB')
		table.add_row('[bold]Ratio', f'[magenta]{self.ratio:.4f}%')
		table.add_row('[bold]Space saved', f'[magenta]{self.space_saved / 1024 / 1024:.4f}MB')
		table.add_row('[bold]Elapsed time', f'[magenta]{self.elapsed:.4f}s')
		yield Panel.fit(table, title='[bold]Compression metrics', style='blue')


class DecompressionMetric(BaseModel):
	file: FileMetric
	elapsed: float

	def __rich_console__(self, console: Console, options: ConsoleOptions):
		yield f'[bold green] Done with compression [magenta]{self.file.filename}[/magenta] in [magenta]{self.elapsed}s[/bold green]'
