import pytest
from compresslib.algorithms.lzw import LZWCoding


@pytest.fixture()
def lzw():
	lzw = LZWCoding('test.txt', 'test')
	return lzw


def test_compress(lzw):
	case = 'TOBEORNOTTOBEORTOBEORNOT'
	res = lzw._compress(case)
	expected_value = [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
	assert res == expected_value


def test_decompress(lzw):
	case = [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
	res = lzw._decompress(case)
	expected_value = 'TOBEORNOTTOBEORTOBEORNOT'
	assert res == expected_value
