import unittest
from unittest.mock import patch, mock_open
from ..algorithms.huffman import HuffmanCoding
from io import BytesIO
import os


class TestHuffmanCoding(unittest.TestCase):
	def setUp(self):
		self.path = 'test.txt'
		self.directory = os.path.dirname(os.path.abspath(__file__))
		self.huffman = HuffmanCoding(self.path, self.directory)

	def test_calculate_frequency(self):
		data = b"aaabbcc"
		with patch('builtins.open', mock_open(read_data=data)) as mocked_file:
			frequency = self.huffman._HuffmanCoding__calculate_frequency()
			expected_frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 2}
			self.assertEqual(frequency, expected_frequency)

	def test_build_heap(self):
		frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 2}
		self.huffman._HuffmanCoding__build_heap(frequency)
		self.assertEqual(len(self.huffman.heap), len(frequency))
		self.assertTrue(all(isinstance(node, HuffmanCoding.HeapNode) for node in self.huffman.heap))

	def test_merge_nodes(self):
		frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 1}
		self.huffman._HuffmanCoding__build_heap(frequency)
		self.huffman._HuffmanCoding__merge_nodes()
		self.assertEqual(len(self.huffman.heap), 1)

	def test_build_codes(self):
		frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 1}
		self.huffman._HuffmanCoding__build_heap(frequency)
		self.huffman._HuffmanCoding__merge_nodes()
		self.huffman._HuffmanCoding__build_codes()
		self.assertTrue(isinstance(self.huffman.codes, dict))
		self.assertTrue(isinstance(self.huffman.reverse_mapping, dict))

	def test_get_encoded_text(self):
		frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 1}
		self.huffman._HuffmanCoding__build_heap(frequency)
		self.huffman._HuffmanCoding__merge_nodes()
		self.huffman._HuffmanCoding__build_codes()
		data = b"aaabbcc"
		with patch('builtins.open', mock_open(read_data=data)) as mocked_file:
			encoded_text = self.huffman._HuffmanCoding__get_encoded_text(data)
			expected_encoded_text = b"\x03\x02\x02\x03\x03\x02\x03\x02\x02"


if __name__ == '__main__':
	unittest.main()
