"""
Plug in for sending SMS messages via the Twilio service.

Only expecting to implement a Target object.  Not clear how a Source object
would work.

The Twilio credentials are stored in the file "twilio.secret".  This file is
not sent to the git repo for obvious reasons!  

The JSON config looks like this:

    {    
      "target":  {
        "type": "twilioplug",
        "to_phone_number": "+4412345678",
        "from_phone_number": "+4412345678"
        }
    }
"""

from mcpi.block import Block
import rube
from twilio.rest import TwilioRestClient

class TwilioplugTarget(rube.Target): #pylint: disable=R0903
    """Send an SMS in response to the update method"""
    def __init__(self, attribs):
        super(TwilioplugTarget, self).__init__()
        self.account_sid=""
        self.auth_token=""
        with open("twilio.secret", "r") as config_file:
            config = config_file.read()
        self.parse_config(config)
        self.from_phone_number = attribs["from_phone_number"]
        self.to_phone_number = attribs["to_phone_number"]
        
    def parse_config(self, config):
        """Set up the object attributes based on the config"""
        allowed_names=["account_sid", "auth_token"]
        for line in config.split("\n"):
            if "=" not in line:
                continue
            name, value = line.split("=")
            if name in allowed_names:
                setattr(self, name, value.rstrip())
            else:
                raise ValueError("Couldn't parse config: " + line)

    def update_state(self, new_state):
        """Send a message via Twilio"""
        client = TwilioRestClient(self.account_sid, self.auth_token)
        body = "New state = " + str(new_state)
        print("Sending message")
        message = client.messages.create(body=body,
                               to=self.to_phone_number,
                               from_=self.from_phone_number)
        
        print(message.sid)