"""
Adaptor for minecraft using Bukkit and the Raspberry Juice plugin

"""

import collections
from mcpi.minecraft import Minecraft
import mcpi.block as block
import rube


MinecraftCoordinates = collections.namedtuple("MinecraftCoordinates", "x y z") # pylint: disable=C0103, C0301

class MinecraftSource(rube.Source): #pylint: disable=R0903
    """Monitor a minecraft server for the block state at given coordinates"""
    def __init__(self, attribs):
        super(MinecraftSource, self).__init__()
        self.server_address = attribs["server_address"]
        self.server_port = attribs.get("server_port", 4711)
        self.coords_x = attribs["coords_x"]
        self.coords_y = attribs["coords_y"]
        self.coords_z = attribs["coords_z"]
        self.world_connection = Minecraft.create(self.server_address,
                                                 self.server_port)

    def poll_state(self):
        """Return the block value from the connected Minecraft server"""
        block_ = self.world_connection.getBlock(self.coords_x,
                                               self.coords_y,
                                               self.coords_z)
        print "Got " + str(block_)
        return block_

class MinecraftTarget(rube.Target): #pylint: disable=R0903
    """Set the block on the server to the specified value"""
    def __init__(self, attribs):
        super(MinecraftTarget, self).__init__()
        self.server_address = attribs["server_address"]
        self.server_port = attribs.get("server_port", 4711)
        self.coords_x = attribs["coords_x"]
        self.coords_y = attribs["coords_y"]
        self.coords_z = attribs["coords_z"]
        self.world_connection = Minecraft.create(self.server_address,
                                                 self.server_port)

    def update_state(self, block_):
        self.world_connection.setBlock(self.coords_x,
                                       self.coords_y,
                                       self.coords_z,
                                       block_)


if __name__ == "__main__":
    JSON_CONFIG = ""
    with open("config.json", "r") as f:
        JSON_CONFIG = f.read()
    
    CONFIG = rube.ConfigJsonParser.parse(JSON_CONFIG)
    SOURCE = CONFIG[0][0]
    SOURCE.world_connection.setBlock(1,
                                     10,
                                     3,
                                     block.TNT)
    CONTROLLER = rube.RubeController(CONFIG)
    CONTROLLER.run_event_loop()
