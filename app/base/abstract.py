from abc import ABC, abstractmethod
from .metric_model import CompressionMetric, DecompressionMetric
from pathlib import Path


class AbstractAlgorithm(ABC):
	def __init__(self, path: str, directory: str, **kwargs):
		self.suffix = kwargs.get('suffix', '.algo')
		self.path: str = path
		self.directory = directory
		self.dir_for_archive = path
		self.base_name = Path(path).stem

	@abstractmethod
	def compress(self, **kwargs):
		pass

	@abstractmethod
	def decompress(self, **kwargs):
		pass

	@abstractmethod
	def compress_archive(self, **kwargs):
		pass

	@abstractmethod
	def decompress_archive(self, **kwargs):
		pass


class AbstractBuilder(ABC):
	def __init__(self, filename: Path, algorithm: AbstractAlgorithm, output: Path):
		self.filename = filename
		self.algorithm = algorithm
		self.output = output

	@abstractmethod
	def compression_metrics(self, **kwargs) -> CompressionMetric:
		pass

	@abstractmethod
	def decompression_metrics(self, **kwargs) -> DecompressionMetric:
		pass

	@abstractmethod
	def execute_compression(self, **kwargs) -> CompressionMetric:
		pass

	@abstractmethod
	def execute_decompression(self, **kwargs) -> DecompressionMetric:
		pass
