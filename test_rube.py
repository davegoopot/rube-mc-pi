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
        
class MockSource(rube.Source):
    
    def poll_state(self):
        return 1
        
        
class MockTarget(rube.Target):
    
    def update_state(self, block):
        self.last_state_update = block

    
    