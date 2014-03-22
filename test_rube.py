import rube
import unittest


class TestRube(unittest.TestCase):

	def setUp(self):
		self.source = MockSource()

	def test_poll_state(self):
		self.source.state = 1
		self.assertEqual(self.source.poll_state(), 1)
	
	def test_update_state(self):
		target = MockTarget()
		target.update_state(1)
		self.assertEqual(target.last_state_update, 1)
	
	def test_event_loop(self):
		target = MockTarget()
		config = ( (self.source, target),  )
		controller = rube.RubeController(config)
		controller.update_all_once()
		self.assertTrue(self.source.was_poll_state_called)
	
	
        
class MockSource(rube.Source):
    
    def __init__(self):
    	self.was_poll_state_called = False
    
    def poll_state(self):
    	self.was_poll_state_called = True
        return 1
        
        
class MockTarget(rube.Target):
    
    def update_state(self, block):
        self.last_state_update = block

    
    