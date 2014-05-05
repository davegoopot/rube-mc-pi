"""Unit testing for the Twilio plugin to send SMS"""

from rube_mc_pi.twilio import TwilioTarget
import StringIO
import unittest


class TestTwilio(unittest.TestCase): # pylint: disable=R0904
    """ All the unittests for the Twilio plugin
    """

    def test_load_config(self): # pylint: disable=C0111
        mock_config = """
account_sid=123456
auth_token=blahblah
"""
        target = TwilioTarget(mock_config)
        self.assertEquals("123456", target.account_sid)
        self.assertEquals("blahblah", target.auth_token)
        
        #Refactor parsing
        
        #Other attribute
        
        #Error on unknown config
        
        #make sure strip whitespace at end
        
        