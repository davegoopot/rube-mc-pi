"""
Adaptor for Raspberry Pi GPIO plugs.

The JSON config looks like this:

    { "source": {
        "type": "gpio",
        "pin": 18,
        "low_state_block": [0, 0],
        "high_state_block": [45, 0]
        },
        
      "target":  {
        "type": "gpio",
        "pin": 12
        }
    }
"""

from mcpi.block import Block
import RPi.GPIO as GPIO
import rube



class GpioSource(rube.Source): #pylint: disable=R0903
    """
        Use the input from the raspberry pi GPIO pin.
		The low_state_block is the block to report if the pin in low
		The high_state_block is what to report if the pin is high
    """
    
    @staticmethod
    def gpio_in_setup(pin):
        """Set the pin up for input"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    
    def __init__(self, attribs):
        super(GpioSource, self).__init__()
        self.pin = attribs["pin"]
        self.low_state_block = Block(attribs["low_state_block"][0], attribs["low_state_block"][1])
        self.high_state_block = Block(attribs["high_state_block"][0], attribs["high_state_block"][1])
        GpioSource.gpio_in_setup(self.pin)

    def poll_state(self):
        if GPIO.input(self.pin):
            return self.high_state_block
        else:
            return self.low_state_block

