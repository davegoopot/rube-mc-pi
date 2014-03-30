"""
Adaptor for minecraft using Bukkit and the Raspberry Juice plugin

"""

import collections
from mcpi.minecraft import Minecraft
import rube


MinecraftCoordinates = collections.namedtuple("MinecraftCoordinates", "x y z") # pylint: disable=C0103, C0301

class MinecraftSource(rube.Source):
    """Monitor a minecraft server for the block state at given coordinates"""
    def __init__(self, server_address, coords, server_port=4711):
        super(MinecraftSource, self).__init__()
        self.server_address = server_address
        self.server_port = server_port
        self.coords = coords
        self.world_connection = Minecraft.create(self.server_address, 
                                                 self.server_port)
        
    def poll_state(self):
        """Return the block value from the connected Minecraft server"""
        block = self.world_connection.getBlock(self.coords.x, 
                                               self.coords.y, 
                                               self.coords.z)
        print "Got " + str(block)
        return block

class MinecraftTarget(rube.Target):
    """Set the block on the server to the specified value"""
    def __init__(self, server_address, coords, server_port=4711):
        super(MinecraftTarget, self).__init__()
        self.server_address = server_address
        self.server_port = server_port
        self.coords = coords
        self.world_connection = Minecraft.create(self.server_address, 
                                                 self.server_port)

    
    def update_state(self, block):
        self.world_connection.setBlock(self.coords.x, 
                                       self.coords.y, 
                                       self.coords.z, 
                                       block)
    
        
if __name__ == "__main__":
    SOURCE_COORDS = MinecraftCoordinates(x=1, y=10, z=3)
    SOURCE = MinecraftSource("localhost", SOURCE_COORDS)
    TARGET_COORDS = MinecraftCoordinates(x=2, y=10, z=3)
    TARGET = MinecraftTarget("localhost", TARGET_COORDS)
    CONFIG = ( (SOURCE, TARGET), )
    SOURCE.world_connection.setBlock(SOURCE.coords.x,
                                     SOURCE.coords.y,
                                     SOURCE.coords.z, 
                                     2)
    CONTROLLER = rube.RubeController(CONFIG)
    CONTROLLER.run_event_loop()
