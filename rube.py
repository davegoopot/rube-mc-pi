"""Code to manage the Rube Goldberg project for the Manchester CoderDojo """

import collections
import json
import time

class RubeController(object):
    """"Responsible for controlling the interactions between components in
    the Rube Goldberg machine.
    """

    def __init__(self, config, min_loop_duration_ms=100):
        """Set up a controller using the passed config.

        The config is a tuple of (source, target) pairs.
        """
        self.config = config
        self.min_loop_duration_ms = min_loop_duration_ms

    def run_event_loop(self):
        """Run the event loop continuously looking for state changes"""
        
        self.record_initial_states()
        while True:
            start_time = time.time()
            self.update_all_once()
            loop_run_time_ms = (time.time() - start_time) * 1000
            if loop_run_time_ms < self.min_loop_duration_ms:
                sleep_needed = (self.min_loop_duration_ms - loop_run_time_ms) \
                               /1000
                time.sleep(sleep_needed)            
            
    def record_initial_states(self):
        """Record the initial state but don't trigger any update"""
        
        for (source, target) in self.config:
            target.last_state_update =  source.poll_state()
        
    def update_all_once(self):
        """Run through all the config pairs once checking state and updating """
        
        for (source, target) in self.config:
            new_state = source.poll_state()
            if target.last_state_update != new_state:
                target.update_state(new_state)
                target.last_state_update = new_state

class Source(object):
    """A source object represents the part of the machine that will trigger the 
    next step when it completes.

    A source adaptor is responsible for responding to the poll_state() method by 
    returning the current state of the source part of the machine.
    
    """
    
    def poll_state(self):
        """Ask a source component for its current state"""
        raise NotImplementedError(
        "It is for concrete implementations of this class to fill in the" \
        "poll_state() method.")
        
        
        
class Target(object):
    """
    A target object represents the part of the machine that should be triggered
    to start of the next step running.
    
    A target adaptor is responsible for responding to the update_state(block) 
    method by taking appropriate actions to update its state.
    
    """
    
    def __init__(self):
        self.last_state_update = "test"
    
    def update_state(self, block):
        """Ask the target component to set its state to the passed Minecraft 
        Block object value."""
        raise NotImplementedError("It is for concrete implementations of this" \
            "class to fill in the update_state(block) method.")

            

ConfigPair = collections.namedtuple("ConfigPair", "source target") # pylint: disable=C0103, C0301
            
class ConfigJsonParser(object):
    """Responsible for reading in JSON config and converting it to a config
    object that can set up the RubeController
    
    """
    
    def parse(self, json_string):
        """Take the json and return (source, target) pairs ready for use"""

        config = [ ]
        jsonparse = json.loads(json_string)
        for config_pair in jsonparse:
            source_module_name = config_pair["source"]["type"] 
            source_module = __import__(source_module_name)
            source_class_name = source_module_name.capitalize() + "Source"
            source_class = getattr(source_module, source_class_name)
            source = source_class()
            source.state = config_pair["source"]["state"]
            source.query_count = config_pair["source"]["query_count"]
            
            target_module_name = config_pair["target"]["type"] 
            target_module = __import__(target_module_name)
            target_class_name = target_module_name.capitalize() + "Target"
            target_class = getattr(target_module, target_class_name)
            target = target_class()
            target.name = config_pair["target"]["name"]
            config.append(ConfigPair(source=source, target=target))
        
        return config   
