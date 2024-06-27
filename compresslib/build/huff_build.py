from ..algorithms.huffman import HuffmanCoding
from ..base.metric_model import CompressionMetric, FileMetric, DecompressionMetric
from ..base.abstract import AbstractBuilder, AbstractAlgorithm
from ..utils.path_utils import get_size
from pathlib import Path
from typing import Type
from time import time
import timeit


class HuffBuild(AbstractBuilder):
	def __init__(self, directory: Path, file: Path, algorithm: Type[AbstractAlgorithm] = HuffmanCoding):
		super().__init__(algorithm=algorithm(directory=str(directory), path=str(file)),
		                 filename=file, output=directory)

	def compression_metrics(self, elapsed: float) -> CompressionMetric:
		original_file = FileMetric(filename=str(self.filename), size=get_size(self.filename))
		compressed_file = FileMetric(filename=str(self.output.joinpath(self.filename.name).with_suffix(self.algorithm.suffix)),
		                             size=get_size(self.output.joinpath(self.filename.name).with_suffix(self.algorithm.suffix)))
		ratio = (compressed_file.size / original_file.size) * 100
		space_saved = original_file.size - compressed_file.size
		return CompressionMetric(file=original_file, compressed_file=compressed_file, ratio=ratio,
		                         space_saved=space_saved, elapsed=elapsed)

	def decompression_metrics(self, elapsed: float) -> DecompressionMetric:
		file = FileMetric(filename=str(self.filename), size=get_size(self.filename))
		return DecompressionMetric(file=file, elapsed=elapsed)

	def execute_func(self):
		if self.filename.suffix == self.algorithm.suffix:
			return self.execute_decompression
		else:
			return self.execute_compression

	def execute_compression(self):
		if self.filename.is_file():
			elapsed = timeit.timeit(self.algorithm.compress, number=1)
		else:
			elapsed = timeit.timeit(self.algorithm.compress_archive, number=1)
		return elapsed

	def execute_decompression(self):
		try:
			elapsed = timeit.timeit(self.algorithm.decompress, number=1)
		except AttributeError:
			elapsed = timeit.timeit(self.algorithm.decompress_archive, number=1)
		return elapsed

	def execute(self, func):
		elapsed = func()
		if func == self.execute_compression:
			return self.compression_metrics(elapsed)
		else:
			return self.decompression_metrics(elapsed)
