"""This module is an example of a plugin implementation and also used for
unittesting.
 """        

import rube
 
class Mock2Source(rube.Source):
    """Stand in for a real source object, counting times called and updating
    as requested by the test methods.
    """
    def __init__(self):
        super(Mock2Source, self).__init__()
        self.attrib1 = None
        self.attrib2 = None

    def poll_state(self):
        pass
        
        
        
        
class Mock2Target(rube.Target):
    """Stand in for a real target object.  Takes record of calls made to update
    """
    def __init__(self):
        super(Mock2Target, self).__init__()
        self.attrib1 = None
        self.attrib2 = None
        self.attrib3 = None

    
    def update_state(self, block):
        pass

    
    
