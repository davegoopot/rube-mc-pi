"""Unit testing for the GPIO plugin -- this will only run on a Raspberry Pi"""


from mcpi.block import Block
import rube
import unittest

try:
    import gpio
    #Only go ahead if gpio is available

    class TestGpio(unittest.TestCase): # pylint: disable=R0904
        """ All the unittests for the GPIO plugin
        """

    
        def test_gpio_plugin_source(self): # pylint: disable=C0111
            json = """
    [
         { "source": {
            "type": "gpio",
            "pin": 18,
            "low_state_block": [0, 0],
            "high_state_block": [45, 2]
            },
        
          "target": {
            "type": "mock",
            "name": "test1"
            }
        }
    ]
    """
            gpio.GpioSource.gpio_in_setup = mock_pin_setup 
            config = rube.ConfigJsonParser.parse(json)
            source = config[0].source
            self.assertEquals(source.pin, 18)
            self.assertEquals(source.low_state_block, Block(0, 0))
            self.assertEquals(source.high_state_block, Block(45, 2))

            gpio.GPIO.input = mock_gpio_pin_high
            state = source.poll_state()
            self.assertEquals(45, state.id)
            self.assertEquals(2, state.data)

            gpio.GPIO.input = mock_gpio_pin_low
            state = source.poll_state()
            self.assertEquals(0, state.id)
            self.assertEquals(0, state.data)

        def test_gpio_plugin_target(self): # pylint: disable=C0111
            json = """
    [
         { "source": {
            "type": "mock",
            "name": "test"
            },
        
          "target": {
            "type": "gpio",
            "pin": 12
            }
        }
    ]
    """
            gpio.GpioTarget.gpio_out_setup = mock_pin_setup 
            config = rube.ConfigJsonParser.parse(json)
            target = config[0].target
            self.assertEquals(target.pin, 12)
            
            
		

except ImportError, ex:
    if ex.message.find("RPi.GPIO") >= 0:
        print "Can't import RPi.GPIO; skipping gpio tests"
    else:
        raise


@staticmethod
def mock_pin_setup(pin):
    """For monkey patching"""
    pass
	
def mock_gpio_pin_high(pin):
    """For monkey patching"""
    return True
    
def mock_gpio_pin_low(pin):
    """For monkey patching"""
    return False
