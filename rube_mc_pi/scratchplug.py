"""
Adaptor for scratch using the scratchpy interface

The JSON config looks like this:

    { "source": {
        "type": "scratchplug",
        "server_address": "localhost",
        "server_port": 42001 
        },
        
      "target":  {
        "type": "scratchplug",
        "server_address": "localhost",
        "server_port": 42001 
        }
    }

"""

import mcpi.block as block
import rube
import scratch as scratch_ex


class ScratchplugSource(rube.Source): #pylint: disable=R0903
    """Wait for a broadcast from scratch showing that the block has changed"""
    pass

class ScratchplugTarget(rube.Target): #pylint: disable=R0903
    """Send a broadcast to scratch with either "BLOCK_PRESENT" or "BLOCK_ABSENT"
    """
    def __init__(self, attribs):
        super(ScratchplugTarget, self).__init__()
        self.scratch_link = ScratchLink(attribs)

    def update_state(self, block_):
        if block_ != block.AIR:
            self.scratch_link.scratch_connection.broadcast("BLOCK_PRESENT")
        else:
            self.scratch_link.scratch_connection.broadcast("BLOCK_ABSENT")

                                    
class ScratchLink(object):
    """
    Responsible for storing the state of the link to a server
    """
                                       
    def __init__(self, attribs):
        self.server_address = attribs["server_address"]
        self.server_port = attribs.get("server_port", 42001)
        self.scratch_connection = scratch_ex.Scratch(self.server_address, port=self.server_port)   
   