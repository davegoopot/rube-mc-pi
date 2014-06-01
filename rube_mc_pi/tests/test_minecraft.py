"""Unit testing for the minecraft plug in"""

from rube_mc_pi.mcpi.minecraft import Minecraft
from rube_mc_pi.minecraft import MinecraftLink
import unittest


class TestMinecraft(unittest.TestCase): # pylint: disable=R0904
    """ All the unittests for the Minecraft plugin
    """

    
    def test_share_world_connection(self): # pylint: disable=C0111
        """The link object should manage connections so that only one connection is created
        to each server.  This connection is shared between all instances that need it."""
        Minecraft.create = mock_create_method
        
        attribs = { "server_address": "test address", 
                           "coords_x" : 1, 
                           "coords_y" : 2, 
                           "coords_z" : 3}
        
        link1 = MinecraftLink(attribs)
        attribs["coords_x"] = 4
        link2 = MinecraftLink(attribs)
        self.assertIs(link1.world_connection,  link2.world_connection)


@staticmethod
def mock_create_method(address = "localhost", port = 4711):
    """Just needs to create unique objects for the purpose of testing object sharing.
    Choose to make """

    from datetime import datetime
    return datetime.now()
