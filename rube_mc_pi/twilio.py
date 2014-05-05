"""
Plug in for sending SMS messages via the Twilio service.

Only expecting to implement a Target object.  Not clear how a Source object
would work.

The Twilio credentials are stored in the file "twilio.secret".  This file is
not sent to the git repo for obvious reasons!  

The JSON config looks like this:

    {    
      "target":  {
        "type": "twilio",
        "phone_number": "+4412345678"
        }
    }
"""

from mcpi.block import Block
import rube

class TwilioTarget(rube.Target): #pylint: disable=R0903
    """Send an SMS in response to the update method"""
    def __init__(self, config):
        super(TwilioTarget, self).__init__()
        self.account_sid=""
        self.auth_token=""
        self.parse_config(config)
        
    def parse_config(self, config):
        """Set up the object attributes based on the config"""
        for line in config.split("\n"):
            if line.startswith("account_sid="):
                self.account_sid = line[len("account_sid="):]
            if line.startswith("auth_token="):
                self.auth_token = line[len("auth_token="):]