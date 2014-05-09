"""
Adaptor for communicating status to and from a http connection.  
The file format is a single line in a file with id,data,  e.g. 123,45

Example JSON config:

     { "source": {
        "type": "http",
        "address": "http://test.com/resource_status"
        },
        
      "target":  {
        "type": "http",
        "address": "http://test.com/update_handler"
        }
    }
"""

from mcpi.block import Block
import rube
import urllib2

class HttpSource(rube.Source): #pylint: disable=R0903
    """Obtain a status update by sending a GET request to an address"""
    def __init__(self, attribs):
        super(HttpSource, self).__init__()
        self.address = attribs["address"]

        
    def poll_state(self):
        response = urllib2.urlopen(self.address).read()
        parsed = response.split(",")
        return Block(id=int(parsed[0]), data=int(parsed[1]))