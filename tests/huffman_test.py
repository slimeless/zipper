from unittest.mock import patch, mock_open

import pytest

from compresslib.algorithms.huffman import HuffmanCoding


@pytest.fixture
def huffman():
	path = str('test.txt')
	directory = str('test')
	return HuffmanCoding(path, directory)


def test_calculate_frequency(huffman):
	data = b"aaabbcc"
	with patch('builtins.open', mock_open(read_data=data)):
		frequency = huffman._HuffmanCoding__calculate_frequency()
		expected_frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 2}
		assert frequency == expected_frequency


def test_build_heap(huffman):
	frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 2}
	huffman._HuffmanCoding__build_heap(frequency)
	assert len(huffman.heap) == len(frequency)
	assert all(isinstance(node, HuffmanCoding.HeapNode) for node in huffman.heap)


def test_merge_nodes(huffman):
	frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 1}
	huffman._HuffmanCoding__build_heap(frequency)
	huffman._HuffmanCoding__merge_nodes()
	assert len(huffman.heap) == 1


def test_build_codes(huffman):
	frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 1}
	huffman._HuffmanCoding__build_heap(frequency)
	huffman._HuffmanCoding__merge_nodes()
	huffman._HuffmanCoding__build_codes()
	assert isinstance(huffman.codes, dict)
	assert isinstance(huffman.reverse_mapping, dict)


def test_get_encoded_text(huffman):
	frequency = {ord('a'): 3, ord('b'): 2, ord('c'): 1}
	huffman._HuffmanCoding__build_heap(frequency)
	huffman._HuffmanCoding__merge_nodes()
	huffman._HuffmanCoding__build_codes()
	data = b"aaabbcc"
	with patch('builtins.open', mock_open(read_data=data)):
		encoded_text = huffman._HuffmanCoding__get_encoded_text(data)
		expected_encoded_text = "00011111010"
		assert encoded_text == expected_encoded_text
