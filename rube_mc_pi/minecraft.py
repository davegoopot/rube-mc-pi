"""
Adaptor for minecraft using Bukkit and the Raspberry Juice plugin

The JSON looks like this:

{ "source": {
        "type": "minecraft",
        "coords_x": 1,
        "coords_y": 10,
        "coords_z": 3,
        "server_address": "localhost"
        },
        
      "target":  {
        "type": "minecraft",
        "coords_x": 2,
        "coords_y": 10,
        "coords_z": 3,
        "server_address": "localhost"
        }


"""

from mcpi.minecraft import Minecraft
import mcpi.block as block
import rube


class MinecraftSource(rube.Source): #pylint: disable=R0903
    """Monitor a minecraft server for the block state at given coordinates"""
    def __init__(self, attribs):
        super(MinecraftSource, self).__init__()
        self.mc_link = MinecraftLink(attribs)

    def poll_state(self):
        """Return the block value from the connected Minecraft server"""
        block_ = self.mc_link.world_connection.getBlock(self.mc_link.coords_x,
                                                        self.mc_link.coords_y,
                                                        self.mc_link.coords_z)
        
        return block_

class MinecraftTarget(rube.Target): #pylint: disable=R0903
    """Set the block on the server to the specified value"""
    def __init__(self, attribs):
        super(MinecraftTarget, self).__init__()
        self.mc_link = MinecraftLink(attribs)

    def update_state(self, block_):
        self.mc_link.world_connection.setBlock(self.mc_link.coords_x,
                                               self.mc_link.coords_y,
                                               self.mc_link.coords_z,
                                               block_)

                                       
class MinecraftLink(object):   #pylint: disable=R0903
    """
    Responsible for storing the state of the link to a server and the location
    of the block that is to be monitored or updated.
    """
                                       
    def __init__(self, attribs):
        self.server_address = attribs["server_address"]
        self.server_port = attribs.get("server_port", 4711)
        self.coords_x = attribs["coords_x"]
        self.coords_y = attribs["coords_y"]
        self.coords_z = attribs["coords_z"]
        self.world_connection = Minecraft.create(self.server_address,
                                              self.server_port)
                                              
if __name__ == "__main__":
    JSON_CONFIG = ""
    with open("config.json", "r") as f:
        JSON_CONFIG = f.read()
    
    CONFIG = rube.ConfigJsonParser.parse(JSON_CONFIG)
    SOURCE = CONFIG[0][0]
    SOURCE.mc_link.world_connection.setBlock(1,
                                             10,
                                             3,
                                             block.TNT)
    CONTROLLER = rube.RubeController(CONFIG)
    CONTROLLER.run_event_loop()
