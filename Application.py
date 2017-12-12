import wx
from LoginWindow import LoginWindow
from StudentListWindow import StudentListWindow
from AddEnrollWindow import AddEnrollWindow


class Application(wx.App):
	__instance = None
	
	@staticmethod
	def instance():
		if not Application.__instance:
			Application.__instance = Application()
		return Application.__instance
	
	def __init__(self):
		"""
		
		"""
		wx.App.__init__(self)
		self.login_window = None
		self.student_list_window = None
		self.add_enroll_window = None
		self.jump_to_login_window(None, None)
	
	# self.jump_to_login_window(None)
	
	def jump_to_login_window(self, parent, data):
		self.jump_to_window(self.login_window, LoginWindow, data, parent)
	
	def jump_to_student_list_window(self, parent, data):
		self.jump_to_window(self.student_list_window, StudentListWindow, data, parent)
	
	def jump_to_add_enroll_window(self, parent, data):
		self.jump_to_window(self.add_enroll_window, AddEnrollWindow, data, parent)
	
	def jump_to_window(self, window, window_class, data, parent):
		if not window:
			window = window_class(parent, data, self)
		window.data = data
		window.parent = parent
		window.Show(True)


app = Application.instance()
app.MainLoop()
