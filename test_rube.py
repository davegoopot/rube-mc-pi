import rube
import unittest


class TestRube(unittest.TestCase):

	def test_getState(self):
		source = MockSource()
		source.state = 1
		self.assertEqual(source.getState(), 1)
		
		
class MockSource(rube.Source):
	
	def getState(self):
		return 1