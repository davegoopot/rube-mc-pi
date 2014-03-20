



class Source(object):
	"""A source object represents the part of the machine that will trigger the next step when it completes.
	
	A source adaptor is responsible for responding to the getState() method by returning the current state of the source part of the machine.
	
	"""
	
	def getState(self):
		raise NotImplementedError("It is for concrete implementations of this class to fill in the getState() method.")
		
		
		
class Target(object):
	"""
	A target object represents the part of the machine that should be triggered to start of the next step running.
	
	A target adaptor is responsible for responding to the updateState(block) method by taking appropriate actions to update its state.
	
	"""
	
	def updateState(self, block):
		raise NotImplementedError("It is for concrete implementations of this class to fill in the updateState(block) method.")
