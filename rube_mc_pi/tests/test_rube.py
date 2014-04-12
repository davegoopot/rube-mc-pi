"""Unit testing module for the whole Rube Goldberg code project"""
from mcpi.block import Block
from rube_mc_pi import *
from rube_mc_pi.mock import MockSource
from rube_mc_pi.mock import MockTarget
import rube_mc_pi.mock2 as mock2
import os.path
from rube_mc_pi.file import FileSource
from rube_mc_pi.file import FileTarget
import rube_mc_pi.rube as rube
import time
import unittest


class TestRube(unittest.TestCase): # pylint: disable=R0904
    """ All the unittests for the rube and associated modules
    """
    def setUp(self):  # pylint: disable=C0103
        nullattribs = {}
        self.source = MockSource(nullattribs)
        self.target = MockTarget(nullattribs)
        self.source2 = MockSource(nullattribs)
        self.target2 = MockTarget(nullattribs)
        self.config = [(self.source, self.target), (self.source2, self.target2)]
        self.controller = rube.RubeController(self.config, 
                                              min_loop_duration_ms = 1)

    def test_poll_state(self): # pylint: disable=C0111
        self.source.state = 1
        self.assertEqual(self.source.poll_state(), 1)
    
    def test_event_loop_calls_poll(self): # pylint: disable=C0111
        self.controller.update_all_once()
        self.assertTrue(self.source.was_poll_state_called)
        self.assertTrue(self.source2.was_poll_state_called)
    
    def test_event_loop_calls_update_on_change(self): # pylint: disable=C0111, C0103, C0301
        self.source.state = 1
        
        self.controller.update_all_once()
        self.source.state = 2
        self.controller.update_all_once()
        self.assertEquals(self.target.last_state_update, 2)

    def test_update_not_called_if_state_doesnt_change(self): # pylint: disable=C0111, C0301, C0103
        self.source.state = 1
        
        self.controller.update_all_once()
        self.target.was_update_state_called = False
        self.controller.update_all_once()
        self.assertFalse(self.target.was_update_state_called)

    def test_event_loop(self): # pylint: disable=C0111
        self.source.state = 1
        self.source.loops_before_stop = 7
        loops_before_change = 2
        new_state = 2   
        self.source.state_changes = { loops_before_change: new_state }
        loops_before_change = 5
        new_state = 99
        self.source.state_changes[loops_before_change] = new_state
        expected_state_log = [2, 99]
        self.run_loop_until_interupt()
        self.assertEquals(self.target.state_log, expected_state_log)

    def test_record_initial_states(self): # pylint: disable=C0111
        self.source2.state = 99
        
        self.controller.record_initial_states()
        self.assertEquals(self.target.last_state_update, self.source.state)
        self.assertEquals(self.target2.last_state_update, self.source2.state)
        
    def run_loop_until_interupt(self): # pylint: disable=C0111
        try:
            self.controller.run_event_loop()
        except KeyboardInterrupt:
            pass
        return
        
    def test_first_event_loop_doesnt_set_state(self): # pylint: disable=C0111, C0301, C0103
        self.source.loops_before_stop = 3
        self.assertEquals(self.target.state_log, [ ])
        self.run_loop_until_interupt()
        
    def test_target_last_state_updated(self): # pylint: disable=C0111
        self.controller.record_initial_states()
        self.source.state = 2
        self.controller.update_all_once()
        self.assertEquals(self.target.last_state_update, 2)
        
        
    def test_json_config_parser(self): # pylint: disable=C0111          
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
        }
    }
]
"""
        
        config = rube.ConfigJsonParser.parse(json)
        expected_source = MockSource({"state":99, "query_count": 200})
        self.assertTrue(config[0].source.was_constructor_called)
        self.assertTrue(config[0].target.was_constructor_called)
        self.assertEquals(config[0].source.state, expected_source.state)
        self.assertEquals(config[0].source.query_count,
                          expected_source.query_count)
        expected_target = MockTarget({"name": "test1"})
        self.assertEquals(config[0].target.name, expected_target.name)

        
    def test_config_two_pairs(self): # pylint: disable=C0111
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
        }
    }
,
	{ "source": {
        "type": "mock",
        "state": 199,
        "query_count": 300
        },
        
      "target": {
        "type": "mock",
        "name": "test2"
        }
    }
]
"""	
        config = rube.ConfigJsonParser.parse(json)
        expected_source1 = MockSource({"state": 99, "query_count": 200})
        self.assertEquals(config[0].source.state, expected_source1.state)
        self.assertEquals(config[0].source.query_count,
                          expected_source1.query_count)
        expected_target1 = MockTarget({"name": "test1"})
        self.assertEquals(config[0].target.name, expected_target1.name)

        expected_source2 = MockSource({"state": 199, "query_count": 300})
        self.assertEquals(config[1].source.state, expected_source2.state)
        self.assertEquals(config[1].source.query_count,
                          expected_source2.query_count)
        expected_target2 = MockTarget({"name": "test2"})
        self.assertEquals(config[1].target.name, expected_target2.name)
        
    def test_rate_limit_event_loop(self): # pylint: disable=C0111
        self.source = MockSource({})
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

    def test_second_mock_json_parser(self): # pylint: disable=C0111
        """Tests that given a dictionary with specific attributes
        the parser sets the values as expected.
        """
        
        attribute_list = {"attrib1": 1, "attrib2": "test"}
        
        source_instance = rube.ConfigJsonParser.make_instance(
                                                "mock2",
                                                "Source",
                                                 attribute_list)
                                                 
        self.assertIsInstance(source_instance, mock2.Mock2Source)
        self.assertEqual(source_instance.attrib1, 1)
        self.assertEqual(source_instance.attrib2, "test")
        
        attribute_list = {"attrib1": 2,
                          "attrib2": "test2", 
                          "attrib3": "test3"}
        target_instance = rube.ConfigJsonParser.make_instance(
                                                "mock2",
                                                "Target",
                                                 attribute_list)
                                                 
        self.assertIsInstance(target_instance, mock2.Mock2Target)
        self.assertEqual(target_instance.attrib1, 2)
        self.assertEqual(target_instance.attrib2, "test2")
        self.assertEqual(target_instance.attrib3, "test3")        
        
    def test_file_plugin_target(self): # pylint: disable=C0111
        file_target = FileTarget({"file_name": "test"})
        self.assertEquals("test", file_target.file_name)
        
        self.assertFalse(os.path.exists("test"))
        block = Block(id=123, data=46)
        try:
            file_target.update_state(block)
            self.assertTrue(os.path.exists("test"))
            with open("test", "r") as file_:
                contents = file_.read()
            self.assertEquals("123,46", contents)
        finally:
            if (os.path.exists("test")):
                os.unlink("test")

    def test_file_plugin_source(self): # pylint: disable=C0111
        file_source = FileSource({"file_name": "test"})
        self.assertEquals("test", file_source.file_name)
        
        try:
            with open("test", "w") as file_:
                file_.write("234,56")
                
            state = file_source.poll_state()
            self.assertEquals(234, state.id)
            self.assertEquals(56, state.data)
        finally:
            if (os.path.exists("test")):
                os.unlink("test")
    
