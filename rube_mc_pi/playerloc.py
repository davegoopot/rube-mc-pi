"""Simple script to print out the (x,y,z) location of the current player on
a minecraft server


usage:  python playerloc.py [server-name] [port]


"""

import rube_mc_pi.mcpi.minecraft as minecraft
import sys


if __name__ == "__main__":
    SERVERNAME = "localhost"
    PORT = 4711
    if len(sys.argv) > 1:
        SERVERNAME = sys.argv[1]
    if len(sys.argv) > 2:
        PORT = int(sys.argv[2])
    print("Opening world '%s:%d'" % (SERVERNAME, PORT))
    WORLD = minecraft.Minecraft.create(SERVERNAME, PORT)
    print("Connected to world")
    POSITION = WORLD.player.getPos()
    print("Player is at (%d, %d, %d)" % (POSITION.x, POSITION.y, POSITION.z))
