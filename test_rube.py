import rube
import unittest


class TestRube(unittest.TestCase):

    def setUp(self):
        self.source = MockSource()
        self.target = MockTarget()
        self.config = [ (self.source, self.target),  ]
        self.controller = rube.RubeController(self.config)

    def test_poll_state(self):
        self.source.state = 1
        self.assertEqual(self.source.poll_state(), 1)
    
    def test_update_state(self):
        self.target.update_state(1)
        self.assertEqual(self.target.last_state_update, 1)

    def test_event_loop_calls_poll(self):
        source2 = MockSource()
        target2 = MockTarget()
        self.config.append((source2, target2) ,)
        
        self.controller.update_all_once()
        self.assertTrue(self.source.was_poll_state_called)
        self.assertTrue(source2.was_poll_state_called)
    
    def test_event_loop_calls_update_on_change(self):
        self.source.state = 1
        
        self.controller.update_all_once()
        self.source.state = 2
        self.controller.update_all_once()
        self.assertEquals(self.target.last_state_update, 2)

    def test_update_not_called_if_state_doesnt_change(self):
        self.source.state = 1
        
        self.controller.update_all_once()
        self.target.was_update_state_called = False
        self.controller.update_all_once()
        self.assertFalse(self.target.was_update_state_called)

    def test_event_loop(self):
        self.source.state = 1
        self.source.loops_before_stop = 7
        loops_before_change = 4
        new_state = 99    
        self.source.state_changes = { loops_before_change: new_state }
        expected_state_log = [1, 99]
        try:
            self.controller.run_event_loop()
        except KeyboardInterrupt:
            pass
        self.assertEquals(self.target.state_log, expected_state_log)

        
class MockSource(rube.Source):
    
    def __init__(self):
        self.was_poll_state_called = False
        self.state = 1
        self.query_count = 0
        self.loops_before_stop = None
        self.state_changes = {}

    def poll_state(self):
        self.was_poll_state_called = True
        self.query_count = self.query_count + 1
        if self.query_count == self.loops_before_stop:
            raise KeyboardInterrupt()
        if self.state_changes.has_key(self.query_count):
            self.state = self.state_changes[self.query_count]
        
        return self.state
        
        
class MockTarget(rube.Target):

    def __init__(self):
        super(MockTarget, self).__init__()
        self.was_update_state_called = False
        self.state_log = []

    
    def update_state(self, block):
        self.last_state_update = block
        self.state_log.append(block)
        self.was_update_state_called = True
        

    
    