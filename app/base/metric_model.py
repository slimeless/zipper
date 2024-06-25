from pydantic import BaseModel
from rich.panel import Panel
from rich.console import Console, ConsoleOptions
from rich.table import Table


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
