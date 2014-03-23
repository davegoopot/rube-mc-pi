"""
Adaptor for minecraft using Bukkit and the Raspberry Juice plugin

"""

from mcpi.minecraft import Minecraft
import rube





class MinecraftSource(rube.Source):

    def __init__(self, server_address,x, y, z, server_port=4711):
        super(rube.Source, self).__init__()
        self.server_address = server_address
        self.server_port = server_port
        self.x = x
        self.y = y
        self.z = z
        self.world_connection = Minecraft.create(self.server_address, self.server_port)
        
    def poll_state(self):
        """Return the block value from the connected Minecraft server"""
        block = self.world_connection.getBlock(self.x, self.y, self.z)
        print "Got " + str(block)
        return block

class MinecraftTarget(rube.Target):
    """TODO:  TESTING VERSION ONLY COPIED FROM MockTarget"""
    def __init__(self):
        super(MinecraftTarget, self).__init__()
        self.was_update_state_called = False
        self.state_log = []

    
    def update_state(self, block):
        self.last_state_update = block
        self.state_log.append(block)
        self.was_update_state_called = True
        
if __name__ == "__main__":
    source = MinecraftSource("w500", x=1, y=2, z=3)
    target = MinecraftTarget()
    config = ( (source, target), )
    controller = rube.RubeController(config)
    controller.run_event_loop()
