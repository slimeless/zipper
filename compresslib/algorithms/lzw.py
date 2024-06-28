import os
import pickle
from collections import defaultdict
from pathlib import Path

from ..base.abstract import AbstractAlgorithm


class LZWCoding(AbstractAlgorithm):
	__slots__ = ('max_table_size', 'compress_dict', 'decompress_dict', 'dict_size', )

	def __init__(self, path: str, directory: str):
		super().__init__(directory=directory, path=path, suffix='.lzw')
		self.max_table_size = 256 ** 2
		self.reset_dictionaries()

	def reset_dictionaries(self):
		self.dict_size = 256
		if Path(self.path).suffix != self.suffix:
			self.compress_dict = defaultdict(lambda: -1, {chr(i): i for i in range(self.dict_size)})
		self.decompress_dict = {i: chr(i) for i in range(self.dict_size)}

	def _compress(self, uncompressed):
		compress_dict = self.compress_dict
		max_table_size = self.max_table_size
		dict_size = self.dict_size

		string = ""
		compressed_data = []
		for symbol in uncompressed:
			string_plus_symbol = string + symbol
			if string_plus_symbol in compress_dict:
				string = string_plus_symbol
			else:
				compressed_data.append(compress_dict.get(string, -1))
				if len(compress_dict) < max_table_size:
					compress_dict[string_plus_symbol] = dict_size
					dict_size += 1
				string = symbol

		if string:
			compressed_data.append(compress_dict.get(string, -1))

		self.dict_size = dict_size

		return compressed_data

	def _decompress(self, compressed):
		compressed = (int(x) for x in compressed)
		string = chr(next(compressed))
		decompressed_data = [string]

		for k in compressed:
			try:
				entry = self.decompress_dict[k]
			except KeyError:
				if k == self.dict_size:
					entry = string + string[0]
				else:
					raise ValueError(f'Bad compressed k: {k}')

			decompressed_data.append(entry)

			if len(self.decompress_dict) < self.max_table_size:
				self.decompress_dict[self.dict_size] = string + entry[0]
				self.dict_size += 1

			string = entry

		return ''.join(decompressed_data)

	def compress(self):
		with open(self.path, 'r') as input_file:
			uncompressed_data = input_file.read()

		compressed_data = self._compress(uncompressed_data)

		with open(self.directory + '/' + self.base_name + self.suffix, 'wb') as output_file:
			pickle.dump((str(Path(self.path).suffix), compressed_data), output_file)

	def decompress(self):
		with open(self.path, 'rb') as input_file:
			file_extension, compressed_data = pickle.load(input_file)

		decompressed_data = self._decompress(compressed_data)
		path_to_save = os.path.join(self.directory, self.base_name + file_extension)
		os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
		with open(path_to_save, 'w') as output_file:
			output_file.write(decompressed_data)

	def _compress_folder(self, folder_path: str) -> dict:
		files_dict = {}
		for root, _, files in os.walk(folder_path):
			for file in files:
				file_path = os.path.join(root, file)
				with open(file_path, 'r') as input_file:
					uncompressed_data = input_file.read()
				compressed_data = self._compress(uncompressed_data)
				relative_path = os.path.relpath(file_path, folder_path)
				files_dict[relative_path] = compressed_data
		return files_dict

	def _decompress_folder(self, files_dict: dict):
		for relative_path, compressed_data in files_dict.items():
			decompressed_data = self._decompress(compressed_data)
			file_path = os.path.join(self.directory, relative_path)
			os.makedirs(os.path.dirname(file_path), exist_ok=True)
			yield file_path, decompressed_data

	def compress_archive(self):
		files_dict = self._compress_folder(self.dir_for_archive)
		archive_name = os.path.basename(self.dir_for_archive) + self.suffix
		with open(archive_name, 'wb') as f:
			pickle.dump(files_dict, f)

	def decompress_archive(self):
		with open(self.dir_for_archive, 'rb') as f:
			files_dict = pickle.load(f)

		for file_path, decompressed_data in self._decompress_folder(files_dict):
			with open(file_path, 'w', encoding='utf-8') as output_file:
				output_file.write(decompressed_data)
