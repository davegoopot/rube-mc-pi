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

from rube_mc_pi.mcpi.block import Block
import rube_mc_pi.rube as rube
import urllib
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
        
class HttpTarget(rube.Target): #pylint: disable=R0903
    """Update the status by sending a POST request with block=new_value"""

    @classmethod
    def build_post_request(cls, block_value):
        """Return the tuple of data, headers suitable for sending to a
        HTTP POST request to update the server to the new block_value"""
        
        data = cls.build_post_data(block_value)
        headers = cls.build_post_headers(data) 
        
        return data, headers

    
    @classmethod
    def build_post_data(cls, block_value):
        """Create the data part of the HTTP POST request to update the block"""
        return urllib.urlencode({'block': block_value})
    
    @classmethod
    def build_post_headers(cls, post_data):
        """Create the HTTP headers to send matching the post_data.
        Assumes that the post_data has already been urlencoded and will not
        be changed again before sending to the server"""
        
        return {"Content-Length": str(len(post_data))}        


        
    def __init__(self, attribs):
        super(HttpTarget, self).__init__()
        self.address = attribs["address"]

    def update_state(self, block_):
        """Send a POST request to update the server"""
        data_to_write = "%d,%d" % (block_.id, block_.data)
        request = urllib2.Request(self.address,
                                  *self.build_post_request(data_to_write))
        response = urllib2.urlopen(request)
        the_page = response.read()
        print("Sent http post.  Response = " + the_page)
        
          
