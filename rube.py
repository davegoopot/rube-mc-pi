"""Code to manage the Rube Goldberg project for the Manchester CoderDojo """



class Source(object):
    """A source object represents the part of the machine that will trigger the 
	next step when it completes.
    
    A source adaptor is responsible for responding to the poll_state() method by 
	returning the current state of the source part of the machine.
    
    """
    
    def poll_state(self):
        """Ask a source component for its current state"""
        raise NotImplementedError(
		"It is for concrete implementations of this class to fill in the" \
		"poll_state() method.")
        
        
        
class Target(object):
    """
    A target object represents the part of the machine that should be triggered
	to start of the next step running.
    
    A target adaptor is responsible for responding to the update_state(block) 
	method by taking appropriate actions to update its state.
    
    """
    
    def update_state(self, block):
        """Ask the target component to set its state to the passed Minecraft 
        Block object value."""
        raise NotImplementedError("It is for concrete implementations of this" \
			"class to fill in the update_state(block) method.")
