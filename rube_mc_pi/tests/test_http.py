"""Unit testing for the http plug in"""

import rube_mc_pi.http as http
from rube_mc_pi.http import HttpSource, HttpTarget
import StringIO
import unittest


class TestHttp(unittest.TestCase): # pylint: disable=R0904
    """ All the unittests for the Http plugin
    """

    def setUp(self): # pylint: disable=C0103
        self.target = HttpTarget({"address": "http://localhost/"})
    
    def test_http_plugin_source(self): # pylint: disable=C0111
        http_source = HttpSource({"address": "http://localhost/"})
        self.assertEquals("http://localhost/", http_source.address)
        http.urllib2.urlopen = mock_urlopen
        
        result = http_source.poll_state()
        self.assertEquals(result.id, 1)
        self.assertEquals(result.data, 2)
        
    def test_http_plugin_target(self): # pylint: disable=C0111
        http_target = self.target
        self.assertEquals("http://localhost/", http_target.address)
        
        new_block = "123,6"
        data, headers = http_target.build_post_request(new_block)
        expected_data = "block=123%2C6"
        self.assertEquals(expected_data, data)
        self.assertEquals(str(len(expected_data)), headers["Content-Length"])
        
    def test_build_post_data(self): # pylint: disable=C0111
        http_target = self.target
        
        new_block = "1,2"
        actual_data = http_target.build_post_data(new_block)
        expected_data = "block=1%2C2"
        self.assertEquals(expected_data, actual_data)
        
        new_block = ""
        actual_data = http_target.build_post_data(new_block)
        expected_data = "block="
        self.assertEquals(expected_data, actual_data)
        
        
    def test_build_post_headers(self): # pylint: disable=C0111
        data = "block=1%2C2"
        actual_headers = self.target.build_post_headers(data)
        self.assertEquals(str(len(data)), actual_headers["Content-Length"])
        
        data = "block="
        actual_headers = self.target.build_post_headers(data)
        self.assertEquals(str(len(data)), actual_headers["Content-Length"])
        
        
        # null
        # 0
        # 1
        # 3
        # lots
        
        
        
        # Test on the demo server
        
        
        
        # Add to the example config
        

def mock_urlopen(url):  # pylint: disable=W0613
    """Used for monkey patch the URL openner 
    for the unit tests of http plugin"""
    return StringIO.StringIO("1,2")

