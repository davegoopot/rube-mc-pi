"""
Adaptor for communicating status to and from a file.  The file format is a 
single line in a file with id,data,  e.g. 123,45

The JSON config looks like this:

    { "source": {
        "type": "file",
        "file_name": "test.txt"
        },
        
      "target":  {
        "type": "file",
        "file_name": "test.txt"
        }
    }
"""

from mcpi.block import Block
import rube

class FileTarget(rube.Target): #pylint: disable=R0903
    """Write the update out to the file"""
    def __init__(self, attribs):
        super(FileTarget, self).__init__()
        self.file_name = attribs["file_name"]
        
    def update_state(self, block_):
        with open(self.file_name, "w") as file_:
            file_.write("%d,%d" % (block_.id, block_.data))

class FileSource(rube.Source): #pylint: disable=R0903
    """Check the status by reading the file"""
    def __init__(self, attribs):
        super(FileSource, self).__init__()
        self.file_name = attribs["file_name"]
        
    def poll_state(self):
        with open(self.file_name, "r") as file_:
            contents = file_.read()
        parsed = contents.split(",")
        return Block(id=int(parsed[0]), data=int(parsed[1]))