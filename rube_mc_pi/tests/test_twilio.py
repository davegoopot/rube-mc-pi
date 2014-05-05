"""Unit testing for the Twilio plugin to send SMS"""

import os
from rube_mc_pi.twilio import TwilioTarget
import StringIO
import unittest


class TestTwilio(unittest.TestCase): # pylint: disable=R0904
    """ All the unittests for the Twilio plugin
    """

    @classmethod
    def setUpClass(cls): # pylint: disable=C0103 
        with open("twilio.secret", "w") as config_file:
            config_file.write("""
account_sid=554436   
auth_token=blahblahbeans      
""")

    @classmethod
    def tearDownClass(cls):  # pylint: disable=C0103
        os.remove("twilio.secret")
            
    
    def test_load_config(self): # pylint: disable=C0111
        mock_config = """
account_sid=123456   
auth_token=blahblah     
"""
        target = TwilioTarget()
        target.parse_config(mock_config)
        self.assertEquals("123456", target.account_sid)
        self.assertEquals("blahblah", target.auth_token)
       
        broken_config = """
no_such_attrib=broken        
"""
        with self.assertRaises(ValueError):
            target.parse_config(broken_config)
        

    def test_load_config_from_file(self): # pylint: disable=C0111
        target = TwilioTarget()
        self.assertEquals("554436", target.account_sid)
        self.assertEquals("blahblahbeans", target.auth_token)
        
        
        