



class Source(object):
	"""A source object represents the part of the machine that will trigger the next step when it completes.
	
	A source adaptor is responsible for responding to the getState() method by returning the current state of the source part of the machine.
	
	"""
	
	def getState(self):
		raise NotImplementedError("It is for concrete implementations of this class to fill in the getState() method.")