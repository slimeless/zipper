import unittest
from unittest.mock import patch, mock_open
from ..algorithms.lzw import LZWCoding


class TestLZW(unittest.TestCase):
	def setUp(self):
		self.lzw = LZWCoding(path='path', directory='directory')

	def test_compress(self):
		case = 'TOBEORNOTTOBEORTOBEORNOT'
		res = self.lzw._compress(case)
		expected_value = [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
		self.assertEqual(res, expected_value)

	def test_decompress(self):
		case = [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
		res = self.lzw._decompress(case)
		expected_value = 'TOBEORNOTTOBEORTOBEORNOT'
		self.assertEqual(res, expected_value)
