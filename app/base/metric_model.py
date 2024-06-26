from pydantic import BaseModel
from rich.panel import Panel
from rich.console import Console, ConsoleOptions
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from typing_extensions import Annotated
from pydantic import BeforeValidator
import traceback

TracebackLocation = Annotated[
	tuple, BeforeValidator(lambda tb: (traceback.extract_tb(tb)[-1].filename, traceback.extract_tb(tb)[-1].lineno))]


class TraceBack(BaseModel):
	traceback: TracebackLocation
	name: str
	message: str

	def __rich_console__(self, console: Console, options: ConsoleOptions):
		tb_align = Align.center(f'file: {self.traceback[0]} line: {self.traceback[1]}', vertical='middle')
		tb_panel = Panel(title='[bold]Traceback location', title_align='center', style='red', renderable=tb_align)
		name_align = Align.center(self.name, vertical='middle')
		name_panel = Panel(title='[bold]Name', title_align='center', renderable=name_align, style='red')
		message_align = Align.center(f'Oops! {self.message}', vertical='middle')
		message_panel = Panel(title='[bold]Message', title_align='center', renderable=message_align, style='red')
		layout_left = Layout(name='left')
		layout_right = Layout(name='right')
		layout_right.split_column(
			Layout(name='upper'),
			Layout(name='lower')
		)
		layout_right['upper'].split_row(Layout(name_panel), Layout(message_panel))
		layout_right['lower'].split_row(Layout(tb_panel))
		layout_right.size = 50
		layout_left.size = 50

		layout = Layout(size=3)
		layout.split_row(layout_left, layout_right)
		yield layout


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
