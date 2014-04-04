"""This module is an example of a plugin implementation and also used for
unittesting.
 """        

import rube
 
class Mock2Source(rube.Source):
    """Stand in for a real source object, counting times called and updating
    as requested by the test methods.
    """
    def __init__(self, **kwargs):
        super(Mock2Source, self).__init__()
        self.attrib1 = kwargs["attrib1"]
        self.attrib2 = kwargs["attrib2"]

    def poll_state(self):
        pass
        
        
        
        
class Mock2Target(rube.Target):
    """Stand in for a real target object.  Takes record of calls made to update
    """
    def __init__(self, **kwargs):
        super(Mock2Target, self).__init__()
        self.attrib1 = kwargs["attrib1"]
        self.attrib2 = kwargs["attrib2"]
        self.attrib3 = kwargs["attrib3"]

    
    def update_state(self, block):
        pass

    
    
