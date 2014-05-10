"""
Adaptor for Arduino Firmata protocol.

NOTE:  This plugin is experimental as there has not been time to test it with
real ardunios at the time of writing.  The plugin is currently a simple port 
of the GPIO code to use the Firmata API.

The JSON config looks like this:

    { "source": {
        "type": "firmata",
        "board": "/dev/tty.usbserial-A6008rIF",
        "pin": 18,
        "low_state_block": [0, 0],
        "high_state_block": [45, 0]
        },
        
      "target":  {
        "type": "firmata",
        "board": "/dev/tty.usbserial-A6008rIF",
        "pin": 12
        }
    }
"""

from rube_mc_pi.mcpi import block
from rube_mc_pi.mcpi.block import Block
import pyfirmata
import rube_mc_pi.rube as rube
import time



class FirmataSource(rube.Source): #pylint: disable=R0903
    """
        Use the input from the firmata pin.
		The low_state_block is the block to report if the pin in low
		The high_state_block is what to report if the pin is high
    """
    
    
    def __init__(self, attribs):
        super(FirmataSource, self).__init__()
        self.low_state_block = Block(attribs["low_state_block"][0], 
                                     attribs["low_state_block"][1])
        self.high_state_block = Block(attribs["high_state_block"][0],
                                      attribs["high_state_block"][1])
        self.board_name = attribs["board"]
        self.board = pyfirmata.Arduino(self.board_name)
        iterator = pyfirmata.util.Iterator(self.board)
        iterator.start()
        time.sleep(1)
        self.pin_number = attribs["pin"]
        self.pin = self.board.get_pin("d:%d:i" % self.pin_number)
        time.sleep(1)
        self.pin.enable_reporting()
        time.sleep(1)

    def poll_state(self):
        if self.pin.read():
            return self.high_state_block
        else:
            return self.low_state_block

class FirmataTarget(rube.Target): #pylint: disable=R0903
    """
        Simply if the state passed is Block.AIR (0,0) the turn output low.
        Any other block type put the output high
    """
            
        
    def __init__(self, attribs):
        super(FirmataTarget, self).__init__()
        self.board_name = attribs["board"]
        self.board = pyfirmata.Arduino(self.board_name)
        time.sleep(1)
        self.pin_number = attribs["pin"]
        self.pin = self.board.get_pin("d:%d:o" % self.pin_number)
        time.sleep(1)
        

    def update_state(self, new_state):
        if new_state == block.AIR:
            self.pin.write(0)
        else:
            self.pin.write(1)
