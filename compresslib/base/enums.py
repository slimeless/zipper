from enum import Enum


class CodingType(str, Enum):
	LZW = 'lzw'
	HUFFMAN = 'huff'
