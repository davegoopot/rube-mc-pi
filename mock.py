"""This module is an example of a plugin implementation and also used for
unittesting.
 """        

import rube
 
class MockSource(rube.Source):
    """Stand in for a real source object, counting times called and updating
    as requested by the test methods.
    """
    def __init__(self, state=1, query_count=0):
        super(MockSource, self).__init__()
        self.was_poll_state_called = False
        self.state = state
        self.query_count = query_count
        self.loops_before_stop = None
        self.state_changes = {}

    def poll_state(self):
        self.was_poll_state_called = True
        self.query_count = self.query_count + 1
        if self.loops_before_stop != None:
            # Need to take account of the intiall poll_state before the 1st loop
            if self.query_count > self.loops_before_stop + 1:  
                raise KeyboardInterrupt()

        if self.state_changes.has_key(self.query_count):
            self.state = self.state_changes[self.query_count]
        
        return self.state
        
        
class MockTarget(rube.Target):
    """Stand in for a real target object.  Takes record of calls made to update
    """
    def __init__(self, name=None):
        super(MockTarget, self).__init__()
        self.was_update_state_called = False
        self.state_log = []
        self.name = name

    
    def update_state(self, block):
        self.state_log.append(block)
        self.was_update_state_called = True
        

    
    
