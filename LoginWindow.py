# -*- coding:utf-8 -*-
import wx
from dao.UserAccessor import UserAccessor


class LoginWindow(wx.Frame):
	def __init__(self, parent, data, app):
		wx.Frame.__init__(self, None,
		                  title=u"登录",
		                  pos=wx.DefaultPosition,
		                  size=wx.Size(300, 350),
		                  style=wx.DEFAULT_FRAME_STYLE)
		self.app = app
		self.data = data
		self.parent = parent
		self.input_username = None
		self.input_userpsw = None
		self.text_prompt = None
		self.btn_login = None
		self.btn_clear = None
		self.__init_widgets()
		self.__init_event()
		self.text_prompt.Hide()
		self.user_accessor = UserAccessor()
	
	def __init_event(self):
		self.Bind(wx.EVT_BUTTON, self.__login, self.btn_login)
		self.Bind(wx.EVT_BUTTON, self.__clear, self.btn_clear)
		self.Bind(wx.EVT_CLOSE, self.__destroy)
	
	def __init_widgets(self):
		"""
		初始化窗口组件
		:return:
		"""
		font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
		layout = wx.BoxSizer(wx.VERTICAL)
		panel = wx.Panel(self)
		panel.SetBackgroundColour("#FFFFFF")
		self.input_username = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_userpsw = wx.TextCtrl(panel, style=wx.TE_LEFT)
		prompt_username = wx.StaticText(panel, label=u"用户名", style=wx.ALIGN_LEFT)
		prompt_username.SetFont(font)
		group_username = wx.BoxSizer(wx.HORIZONTAL)
		group_username.Add(prompt_username, 1, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
		group_username.Add(self.input_username, 2, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL)
		layout.Add(group_username, 0, wx.TOP | wx.FIXED_MINSIZE | wx.ALIGN_CENTER_HORIZONTAL, 50)
		prompt_userpswd = wx.StaticText(panel, label=u"密码", style=wx.TE_PASSWORD)
		prompt_userpswd.SetFont(font)
		group_pswd = wx.BoxSizer(wx.HORIZONTAL)
		group_pswd.Add(prompt_userpswd, 1, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 7)
		group_pswd.Add(self.input_userpsw, 2, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL)
		layout.Add(group_pswd, 0, wx.TOP | wx.FIXED_MINSIZE | wx.ALIGN_CENTER_HORIZONTAL, 20)
		self.btn_login = wx.Button(panel, label=u"登录")
		layout.Add(self.btn_login, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 60)
		self.btn_clear = wx.Button(panel, label=u"清空")
		layout.Add(self.btn_clear, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 60)
		self.text_prompt = wx.StaticText(panel, style=wx.TE_LEFT, label=u"密码错误")
		self.text_prompt.SetFont(font)
		# layout.Add(self.text_prompt, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 60)
		group_prompt = wx.BoxSizer(wx.VERTICAL)
		group_prompt.Add(self.text_prompt, 0, wx.TOP | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 30)
		layout.Add(group_prompt, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 60)
		panel.SetSizer(layout)
	
	def __login(self, event):
		"""
		登陆按钮回调函数
		:param event:
		:return:
		"""
		print("login button clicked")
		username = self.input_username.GetValue()
		if username.strip() == "":
			wx.MessageDialog(self, message=u"用户名不能为空", style=wx.ICON_ERROR | wx.OK).ShowModal()
			return
		elif len(username) > 16:
			wx.MessageDialog(self, message=u"用户名过长", style=wx.ICON_ERROR | wx.OK).ShowModal()
			return
		password = self.input_userpsw.GetValue()
		if password.strip() == "":
			wx.MessageDialog(self, message=u"密码不能为空", style=wx.ICON_ERROR | wx.OK).ShowModal()
			return
		elif len(password) > 16:
			wx.MessageDialog(self, message=u"密码过长", style=wx.ICON_ERROR | wx.OK).ShowModal()
			return
		login_result = self.user_accessor.login(username, password)
		if login_result == -1:
			wx.MessageDialog(self, message=u"密码错误", style=wx.ICON_ERROR | wx.OK).ShowModal()
		elif login_result == -2:
			wx.MessageDialog(self, message=u"用户名不存在", style=wx.ICON_ERROR | wx.OK).ShowModal()
		else:
			self.close()
			self.app.jump_to_student_list_window(None, None)
	
	def __clear(self, event):
		"""
		清空按钮回调函数
		:param event:
		:return:
		"""
		print("clear button clicked")
		self.input_username.Clear()
		self.input_userpsw.Clear()
		pass
	
	def close(self):
		"""
		关闭该窗口
		:return:
		"""
		self.Close(True)
	
	def __destroy(self, event):
		"""
		
		:return:
		"""
		self.Destroy()
