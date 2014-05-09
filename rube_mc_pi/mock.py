"""This module is an example of a plugin implementation and also used for
unittesting.
 """

from rube_mc_pi.rube import Source, Target

class MockSource(Source): #pylint: disable=R0903
    """Stand in for a real source object, counting times called and updating
    as requested by the test methods.
    """
    def __init__(self, attribs):
        super(MockSource, self).__init__()
        self.was_poll_state_called = False
        self.state = attribs.get("state", 1)
        self.query_count = attribs.get("query_count", 0)
        self.loops_before_stop = None
        self.state_changes = {}
        self.was_constructor_called = True

    def poll_state(self):
        self.was_poll_state_called = True
        self.query_count = self.query_count + 1
        if self.loops_before_stop != None:
            # Need to take account of the initial poll_state before the 1st loop
            if self.query_count > self.loops_before_stop + 1:
                raise KeyboardInterrupt()

        if self.state_changes.has_key(self.query_count):
            self.state = self.state_changes[self.query_count]

        return self.state


class MockTarget(Target): #pylint: disable=R0903
    """Stand in for a real target object.  Takes record of calls made to update
    """
    def __init__(self, attribs):
        super(MockTarget, self).__init__()
        self.was_update_state_called = False
        self.state_log = []
        self.name = attribs.get("name", "")
        self.was_constructor_called = True


    def update_state(self, block):
        self.state_log.append(block)
        self.was_update_state_called = True




