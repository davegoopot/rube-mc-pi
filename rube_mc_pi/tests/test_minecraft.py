"""Unit testing for the minecraft plug in"""

from rube_mc_pi.mcpi.minecraft import Minecraft
from rube_mc_pi.minecraft import MinecraftLink
from rube_mc_pi.minecraft import MinecraftSource
from rube_mc_pi.minecraft import MinecraftTarget
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

        attribs["server_address"] = "different address"
        link3 = MinecraftLink(attribs)
        self.assertIsNot(link1.world_connection,  link3.world_connection)
        
        attribs["server_port"] = 1234
        link4 = MinecraftLink(attribs)
        self.assertIsNot(link3.world_connection,  link4.world_connection)

        src1 = MinecraftSource(attribs)
        attribs["coords_x"] = 5
        src2 = MinecraftSource(attribs)
        self.assertIs(src1.mc_link.world_connection,  src2.mc_link.world_connection)

        trg1 = MinecraftTarget(attribs)
        attribs["coords_x"] = 6
        trg2 = MinecraftTarget(attribs)
        self.assertIs(trg1.mc_link.world_connection,  trg2.mc_link.world_connection)
        self.assertIs(trg1.mc_link.world_connection,  src1.mc_link.world_connection)

@staticmethod
def mock_create_method(address = "localhost", port = 4711):
    """Just needs to create unique objects for the purpose of testing object sharing.
    Choose to make """

    from datetime import datetime
    return datetime.now()
