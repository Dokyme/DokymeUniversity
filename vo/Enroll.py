class Enroll(object):
	def __init__(self):
		self.sid = None
		self.grade = None
		self.dname = None
		self.cno = None
		self.sectno = None
		self.section = None
	
	def __eq__(self, o: object) -> bool:
		if isinstance(o, Enroll):
			return self.dname == o.dname and self.cno == o.cno and self.sectno == o.sectno
		else:
			return False
	
	def __ne__(self, o: object) -> bool:
		return not self.__eq__(o)
	
	def __hash__(self) -> int:
		return hash(self.dname) + hash(self.cno) + hash(self.sectno)
