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
        "message_type": "sms"    or could be "call"
        }
    }
"""

from ConfigParser import SafeConfigParser
from rube_mc_pi.mcpi.block import Block
import rube_mc_pi.rube as rube
from twilio.rest import TwilioRestClient

class TwilioplugTarget(rube.Target): #pylint: disable=R0903
    """Send an SMS in response to the update method"""
    def __init__(self, attribs):
        super(TwilioplugTarget, self).__init__()
        self.account_sid = ""
        self.auth_token = ""
        parser = SafeConfigParser()
        parser.read("twilio.secret")
        print(parser)
        
        self.parse_config(parser)

        self.from_phone_number = attribs["from_phone_number"]
        self.to_phone_number = attribs["to_phone_number"]
        self.message_type = attribs["message_type"]
        
    def parse_config(self,  parser):
        """Read the SafeConfigParser object and set up the instance"""
        self.account_sid = parser.get("twilio", "account_sid")
        self.auth_token = parser.get("twilio", "auth_token")
        

    def update_state(self, new_state):
        """Send a message via Twilio"""
        client = TwilioRestClient(self.account_sid, self.auth_token)
        body = "New state = " + str(new_state)
        
        if self.message_type == "call":
            self.call_phone(client)
        elif self.message_type == "sms":
            self.send_sms(client, body)
        else:
            raise RuntimeError("Unknown Twilio message type: " + 
                                self.message_type)
            
    def call_phone(self, client):
        """Use the Twilio API to call the phone and play recorded music"""
        print("Calling phone")
        call = client.calls.create(to=self.to_phone_number,
                                   from_=self.from_phone_number,
                                   url="http://twimlets.com/holdmusic",  
                                   method="GET",  
                                   fallback_method="GET",  
                                   status_callback_method="GET",    
                                   record="false")
        
        print(call.sid)
    
    def send_sms(self, client, body):
        """Use the Twilio API to send an SMS to the phone with the block type"""
        print("Sending message")
        message = client.messages.create(body=body,
                               to=self.to_phone_number,
                               from_=self.from_phone_number)
        
        print(message.sid)
