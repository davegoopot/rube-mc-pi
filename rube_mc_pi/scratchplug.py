"""
Adaptor for scratch using the scratchpy interface

To function as a source, the scratch program should just broadcast a block state
e.g. broadcast 41,0

To function as a target, the scratch program should listen for broadcasts saying
either BLOCK_PRESENT or BLOCK_ABSENT.  Implementation of individual block types
has not yet been implemented

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

import rube_mc_pi.mcpi.block as block
from multiprocessing import Process, Queue
from Queue import Empty
import rube_mc_pi.rube as rube
import scratch as scratch_ex


class ScratchplugSource(rube.Source): #pylint: disable=R0903
    """Wait for a broadcast from scratch showing that the block has changed
    The standard scratch.receive() method blocks until a message is received.
    This implementation wraps the call in a multiprocessing loop to give up
    if nothing is received before a time out
    """
    def __init__(self, attribs):
        super(ScratchplugSource, self).__init__()
        self.scratch_link = ScratchLink(attribs)
        self.last_block_state = block.AIR
        self.from_scratch = None

    def receive_from_scratch(self, queue):
        """Look for a "x,y" broadcast and convert to a block.
        If a broadcast is received that doesn't parse into x,y then leave the
        state unchanged.
        """
        self.from_scratch = None
        received = self.scratch_link.scratch_connection.receive()[1]
        try:
            id_, data = received.split(",")
            _block = block.Block(int(id_), int(data))
        except ValueError:
            #Assume that the broadcast wasn't intended as a block change
            print("Unparsable broadcast:" + received)
            _block = None
            
        if _block:
            queue.put(_block)
        
    def poll_state(self):
        """Assumes that scratch will broadcast "x,y" to represent the
        block state.        
        """
        queue = Queue()
        proc = Process(target=self.receive_from_scratch, args=(queue,))
        proc.start()
     
        timout_secs = 3
        proc.join(timout_secs)

        if proc.is_alive():
            proc.terminate()
            proc.join()
            
        try:
            _block = queue.get_nowait()
            self.last_block_state = _block
        except Empty:
            pass
        
        return self.last_block_state
    
    

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
        self.scratch_connection = scratch_ex.Scratch(self.server_address,
                                                     port=self.server_port)   
   