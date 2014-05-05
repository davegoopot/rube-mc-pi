"""This module is an example of a plugin implementation and also used for
unittesting.
 """

from rube_mc_pi.rube import Source, Target

class Mock2Source(Source): #pylint: disable=R0903
    """Stand in for a real source object, counting times called and updating
    as requested by the test methods.
    """
    def __init__(self, attribs):
        super(Mock2Source, self).__init__()
        self.attrib1 = attribs["attrib1"]
        self.attrib2 = attribs["attrib2"]

    def poll_state(self):
        pass




class Mock2Target(Target): #pylint: disable=R0903
    """Stand in for a real target object.  Takes record of calls made to update
    """
    def __init__(self, attribs):
        super(Mock2Target, self).__init__()
        self.attrib1 = attribs["attrib1"]
        self.attrib2 = attribs["attrib2"]
        self.attrib3 = attribs["attrib3"]


    def update_state(self, block):
        pass



