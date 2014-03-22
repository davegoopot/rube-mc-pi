import rube
import unittest


class TestRube(unittest.TestCase):

    def test_poll_state(self):
        source = MockSource()
        source.state = 1
        self.assertEqual(source.poll_state(), 1)
        
    def test_update_state(self):
        target = MockTarget()
        target.update_state(1)
        self.assertEqual(target.last_state_update, 1)
        
    def test_event_loop(self):
    	source = MockSource()
    	target = MockTarget()
    	config = ( (source, target),  )
    	controller = rube.RubeController(config)
    	controller.update_all_once()
    	self.assertTrue(source.was_poll_state_called)
        
class MockSource(rube.Source):
    
    def __init__(self):
    	self.was_poll_state_called = False
    
    def poll_state(self):
    	self.was_poll_state_called = True
        return 1
        
        
class MockTarget(rube.Target):
    
    def update_state(self, block):
        self.last_state_update = block

    
    