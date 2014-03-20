import rube
import unittest


class TestRube(unittest.TestCase):

	def test_pollState(self):
		source = MockSource()
		source.state = 1
		self.assertEqual(source.pollState(), 1)
		
	def test_updateState(self):
		target = MockTarget()
		target.updateState(1)
		self.assertEqual(target.last_state_update, 1)
		
class MockSource(rube.Source):
	
	def pollState(self):
		return 1
		
		
class MockTarget(rube.Target):
	
	def updateState(self, block):
		self.last_state_update = block

	
	