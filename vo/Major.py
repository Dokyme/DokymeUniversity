class Major(object):
	def __init__(self):
		self.dname = None
		self.sid = None
	
	def __eq__(self, o: object) -> bool:
		if isinstance(o, Major):
			return self.sid == o.sid and self.dname == o.dname
		else:
			return False
	
	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)
	
	def __str__(self) -> str:
		return "({},{})".format(self.sid, self.dname)
	
	def __hash__(self) -> int:
		return hash(self.sid) + hash(self.dname)
