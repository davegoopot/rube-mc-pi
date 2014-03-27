"""Unit testing module for the whole Rube Goldberg code project"""
from mock import MockSource
from mock import MockTarget
import rube  
import sys
import time
import unittest


class TestRube(unittest.TestCase):
    """
    TODO:  Plugin loader from plugins directory
    TODO:  Config to load MockPlugin
    TODO:  Test can load Minecraft plugin with appropriate attributes
    """
    def setUp(self):
        self.source = MockSource()
        self.target = MockTarget()
        self.source2 = MockSource()
        self.target2 = MockTarget()
        self.config = [ (self.source, self.target), (self.source2, self.target2)  ]
        self.controller = rube.RubeController(self.config)

    def test_poll_state(self):
        self.source.state = 1
        self.assertEqual(self.source.poll_state(), 1)
    
    def test_event_loop_calls_poll(self):
        self.controller.update_all_once()
        self.assertTrue(self.source.was_poll_state_called)
        self.assertTrue(self.source2.was_poll_state_called)
    
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
        loops_before_change = 2
        new_state = 2   
        self.source.state_changes = { loops_before_change: new_state }
        loops_before_change = 5
        new_state = 99
        self.source.state_changes[loops_before_change] = new_state
        expected_state_log = [2, 99]
        try:
            self.controller.run_event_loop()
        except KeyboardInterrupt:
            pass
        self.assertEquals(self.target.state_log, expected_state_log)

    def test_record_initial_states(self):
        self.source2.state = 99
        
        self.controller.record_initial_states()
        self.assertEquals(self.target.last_state_update, self.source.state)
        self.assertEquals(self.target2.last_state_update, self.source2.state)
        
    def test_first_event_loop_doesnt_set_state(self):
        self.source.loops_before_stop = 3
        try:
            self.controller.run_event_loop()
        except KeyboardInterrupt:
            pass
        self.assertEquals(self.target.state_log, [ ])
        
        
    def test_target_last_state_updated(self):
        self.controller.record_initial_states()
        self.source.state = 2
        self.controller.update_all_once()
        self.assertEquals(self.target.last_state_update, 2)
        
        
    def test_json_config_parser(self):
        parser = rube.ConfigJsonParser()
             
        json = """
[
     { "source": {
        "type": "mock",
        "state": 99,
        "query_count": 200
        },
        
      "target": {
        "type": "mock",
        "name": "test1"
        },
        }
    }
]
"""
        config = parser.parse(json)
        expected_source = MockSource(state=99, query_count=200)
        self.assertEquals(config[0].source.state, expected_source.state)
        self.assertEquals(config[0].source.query_count, expected_source.query_count)
        expected_target = MockTarget(name="test1")
        self.assertEquals(config[0].target.name, expected_target.name)

        
    def test_rate_limit_event_loop(self): # pylint: disable=C0111
        self.source = MockSource()
        self.source.loops_before_stop = 10
        self.config = [ (self.source, self.target), ]
        self.controller = rube.RubeController(self.config, 
                                              min_loop_duration_ms=100)
        start_time = time.time()
        self.run_loop_until_interupt()
        end_time = time.time()
        run_time = end_time - start_time
        minimum_time = 10 * 100 / 1000   #
        self.assertGreater(run_time, minimum_time)


    # def test_plugin_loader(self):
        # plugin_loader = rube.PluginLoader()
        # plugin_loader.load_from_plugin_dir()
        # self.assertTrue("testplugin" in sys.modules.keys())
    
