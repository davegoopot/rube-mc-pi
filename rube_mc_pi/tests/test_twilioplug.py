"""Unit testing for the Twilio plugin to send SMS"""

import os
from rube_mc_pi import rube
from rube_mc_pi.twilioplug import TwilioplugTarget
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
      
    def setUp(self): # pylint: disable=C0103
        attribs = { "to_phone_number": "1234", "from_phone_number": "5673" }
        self.target = TwilioplugTarget(attribs)
    
    def test_load_config(self): # pylint: disable=C0111
        mock_config = """
account_sid=123456   
auth_token=blahblah     
"""
        self.target.parse_config(mock_config)
        self.assertEquals("123456", self.target.account_sid)
        self.assertEquals("blahblah", self.target.auth_token)
       
        broken_config = """
no_such_attrib=broken        
"""
        with self.assertRaises(ValueError):
            self.target.parse_config(broken_config)
        

    def test_load_config_from_file(self): # pylint: disable=C0111
        self.assertEquals("554436", self.target.account_sid)
        self.assertEquals("blahblahbeans", self.target.auth_token)
        
        
    def test_json_config(self):  # pylint: disable=C0111
        json = """
    [
        {
         "source": {
            "type": "mock"
            }
        ,
          "target": {
            "type": "twilioplug",
            "from_phone_number": "+123456",
            "to_phone_number": "+879"
            }
        }
    ]
    """
        config = rube.ConfigJsonParser.parse(json)
        target = config[0].target
        self.assertEquals(target.from_phone_number, "+123456")
        self.assertEquals(target.to_phone_number, "+879")

if __name__ == '__main__':
    unittest.main()