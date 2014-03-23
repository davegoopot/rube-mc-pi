"""
Adaptor for minecraft using Bukkit and the Raspberry Juice plugin

TODO:  Refactor out server and x,y,z data set

"""

from mcpi.minecraft import Minecraft
import rube


class MinecraftSource(rube.Source):
    """Monitor a minecraft server for the block state at given coordinates"""
    def __init__(self, server_address, x, y, z, server_port=4711):
        super(MinecraftSource, self).__init__()
        self.server_address = server_address
        self.server_port = server_port
        self.x = x
        self.y = y
        self.z = z
        self.world_connection = Minecraft.create(self.server_address, 
                                                 self.server_port)
        
    def poll_state(self):
        """Return the block value from the connected Minecraft server"""
        block = self.world_connection.getBlock(self.x, self.y, self.z)
        print "Got " + str(block)
        return block

class MinecraftTarget(rube.Target):
    """Set the block on the server to the specified value"""
    def __init__(self, server_address, x, y, z, server_port=4711):
        super(MinecraftTarget, self).__init__()
        self.server_address = server_address
        self.server_port = server_port
        self.x = x
        self.y = y
        self.z = z
        self.world_connection = Minecraft.create(self.server_address, 
                                                 self.server_port)

    
    def update_state(self, block):
        self.world_connection.setBlock(self.x, self.y, self.z, block)
        super(MinecraftTarget, self).update_state(block)
    
        
if __name__ == "__main__":
    SOURCE = MinecraftSource("localhost", x=1, y=2, z=3)
    TARGET = MinecraftTarget("localhost", x=5, y=2, z=3)
    CONFIG = ( (SOURCE, TARGET), )
    SOURCE.world_connection.setBlock(SOURCE.x, SOURCE.y, SOURCE.z, 1)
    CONTROLLER = rube.RubeController(CONFIG)
    CONTROLLER.run_event_loop()
