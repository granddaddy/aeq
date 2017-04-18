import unittest
import castles


class TestCastles(unittest.TestCase):

	def test_index_one(self):
		land = castles.Land(10, 10)
		self.assertEqual(land.to1DIndex(0, 0), 0)
		self.assertEqual(land.to1DIndex(0, 5), 5)
		self.assertEqual(land.to1DIndex(9, 0), 90)
		self.assertEqual(land.to1DIndex(9, 9), 99)

		with self.assertRaises(IndexError):
			land.to1DIndex(10, 10)

		with self.assertRaises(IndexError):
			land.to1DIndex(-1, -1)

	def test_index_two(self):
		land = castles.Land(12, 12)
		self.assertEqual(land.to1DIndex(1, 0), 12)
		self.assertEqual(land.to1DIndex(11, 0), 132)
		self.assertEqual(land.to1DIndex(11, 11), 143)

if __name__ == '__main__':
	unittest.main()