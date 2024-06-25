import os
import heapq
from collections import Counter
import pickle
import struct
from ..base.abstract import AbstractAlgorithm
from typing import Optional
from pathlib import Path


class HuffmanCoding(AbstractAlgorithm):

	def __init__(self, directory, path: Optional[str] = None):
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}
		self.tree = None
		super().__init__(suffix='.huff', directory=directory, path=path)

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		def __lt__(self, other):
			return self.freq < other.freq

	def __calculate_frequency(self):
		with open(self.path, 'rb') as f:
			data = f.read()
		frequency = Counter(data)
		return frequency

	def __build_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def __merge_nodes(self):
		while len(self.heap) > 1:
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)

	def __build_codes_helper(self, root, current_code):
		if not root:
			return

		if root.char:
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.__build_codes_helper(root.left, current_code + "0")
		self.__build_codes_helper(root.right, current_code + "1")

	def __build_codes(self):
		root = heapq.heappop(self.heap)
		self.tree = root
		current_code = ""
		self.__build_codes_helper(root, current_code)

	def __get_encoded_text(self, data):
		encoded_text = ''.join(self.codes[byte] for byte in data)
		return encoded_text

	@staticmethod
	def __pad_encoded_text(encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		encoded_text += "0" * extra_padding

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text

	@staticmethod
	def __get_byte_array(padded_encoded_text):
		return bytes([int(padded_encoded_text[i:i + 8], 2) for i in range(0, len(padded_encoded_text), 8)])

	@staticmethod
	def __remove_padding(padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1 * extra_padding]

		return encoded_text

	@staticmethod
	def __get_byte_string(b):
		return ''.join([bin(byte)[2:].rjust(8, '0') for byte in b])

	def __decode_text(self, encoded_text):
		current_node = self.tree
		decoded_text = bytearray()
		tree_root = self.tree

		for bit in encoded_text:
			current_node = current_node.left if bit == "0" else current_node.right

			if current_node.char is not None:
				decoded_text.append(current_node.char)
				current_node = tree_root

		return bytes(decoded_text)

	def _compress(self):
		frequency = self.__calculate_frequency()
		self.__build_heap(frequency)
		self.__merge_nodes()
		self.__build_codes()

		with open(self.path, 'rb') as f:
			data = f.read()

		encoded_text = self.__get_encoded_text(data)
		padded_encoded_text = self.__pad_encoded_text(encoded_text)

		b = self.__get_byte_array(padded_encoded_text)
		file_extension = os.path.splitext(self.path)[1]

		return file_extension, self.tree, b

	def compress(self):
		file_extension, tree, b = self._compress()
		with open(self.base_name + self.suffix, 'wb') as f:
			pickle.dump((file_extension, tree, b), f)

	def _decompress(self):
		with open(self.path, 'rb') as f:
			extension, self.tree, b = pickle.load(f)

		bit_string = self.__get_byte_string(b)

		encoded_text = self.__remove_padding(bit_string)
		decompressed_text = self.__decode_text(encoded_text)

		return extension, decompressed_text

	def decompress(self):
		extension, decompressed_text = self._decompress()
		path_to_save = os.path.join(self.directory, self.base_name + extension)
		os.makedirs(os.path.dirname(path_to_save), exist_ok=True)
		with open(path_to_save, 'wb') as f:
			f.write(decompressed_text)

	def __encode_directory(self, files_dict: dict):
		for root, _, files in os.walk(self.dir_for_archive):
			for file in files:
				file_path = str(os.path.join(root, file))
				self.path = file_path
				file_extension, tree, b = self._compress()
				relative_path = os.path.relpath(self.path, self.dir_for_archive)
				files_dict[relative_path] = (file_extension, tree, b)

	def __decode_directory(self, files_dict: dict):
		for relative_path, (file_extension, tree, b) in files_dict.items():
			self.tree = tree
			full_path = os.path.join(self.directory, relative_path)
			os.makedirs(os.path.dirname(full_path), exist_ok=True)
			decompressed_text = self.__decode_text(
				self.__remove_padding(self.__get_byte_string(b)))
			yield full_path, decompressed_text

	def compress_archive(self):
		files_dict = {}
		self.__encode_directory(files_dict)
		archive_name = os.path.basename(self.dir_for_archive) + self.suffix
		with open(archive_name, 'wb') as f:
			pickle.dump(files_dict, f)

	def decompress_archive(self):
		with open(self.dir_for_archive, 'rb') as f:
			files_dict = pickle.load(f)

		for full_path, decompressed_text in self.__decode_directory(files_dict):
			with open(full_path, 'wb') as f:
				f.write(decompressed_text)
