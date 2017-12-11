# -*- coding:utf-8 -*-
import wx
import wx.grid
from StudentListWindow import CustomedGird
from dao.SectionAccessor import SectionAccessor
from dao.EnrollAccessor import EnrollAccessor


class AddEnrollWindow(wx.Frame):
	def __init__(self, parent, data=None, app=None):
		wx.Frame.__init__(self, None, title=u"选课", pos=wx.DefaultPosition, size=wx.Size(600, 680),
		                  style=wx.DEFAULT_FRAME_STYLE)
		self.app = app
		self.data = data
		self.parent = parent
		self.section_grid = None
		self.section_list = None
		self.btn_cancel = None
		self.btn_add = None
		self.combo_grade = None
		self.enroll_accessor = EnrollAccessor()
		self.__init_widgets()
		self.__init_events()
	
	def __init_widgets(self):
		"""
		
		:return:
		"""
		panel = wx.Panel(self)
		panel.SetBackgroundColour("#FFFFFF")
		layout = wx.BoxSizer(wx.VERTICAL)
		group_grid = wx.BoxSizer(wx.VERTICAL)
		group_btn = wx.BoxSizer(wx.HORIZONTAL)
		self.section_list = SectionList()
		self.section_grid = CustomedGird(panel)
		self.section_grid.init(self.section_list, max_size=wx.Size(650, 800), min_size=wx.Size(650, 500))
		group_grid.Add(self.section_grid, 0, wx.ALL, 5)
		self.combo_grade = wx.ComboBox(panel, wx.ID_ANY, value="1", choices=[str(i) for i in range(1, 6)],
		                               style=wx.CB_READONLY)
		self.btn_cancel = wx.Button(panel, label=u"取消")
		self.btn_add = wx.Button(panel, label=u"添加")
		group_btn.Add(self.combo_grade, 0, wx.ALL, 5)
		group_btn.Add(self.btn_add, 0, wx.ALL, 5)
		group_btn.Add(self.btn_cancel, 0, wx.ALL, 5)
		layout.Add(group_grid, 0, wx.ALL, 5)
		layout.Add(group_btn, 0, wx.ALL, 5)
		panel.SetSizer(layout)
	
	def __init_events(self):
		"""
		
		:return:
		"""
		self.Bind(wx.EVT_BUTTON, self.__add, self.btn_add)
		self.Bind(wx.EVT_BUTTON, self.__cancel, self.btn_cancel)
		self.Bind(wx.EVT_CLOSE, self.__destory)
	
	def __add(self, event):
		rows = self.section_grid.GetSelectedRows()
		if len(rows) == 0:
			wx.MessageDialog(self, u"没有选择开课的项目!", style=wx.OK | wx.ICON_ERROR).ShowModal()
		else:
			row = rows[0]
			section = self.section_list.table[row]
			grade = int(self.combo_grade.GetItems()[self.combo_grade.GetSelection()])
			result = self.enroll_accessor.add_enroll_to_specified_student(self.data["sid"], grade, section)
			if result == 0:
				wx.MessageDialog(self, u"添加选课失败!", style=wx.OK | wx.ICON_ERROR).ShowModal()
			else:
				wx.MessageDialog(self, u"添加选课成功~", style=wx.ICON_INFORMATION | wx.OK).ShowModal()
			self.parent._search_full_info(None)
			self.__cancel(None)
	
	def __cancel(self, event):
		self.Close(True)
	
	def __destory(self, event):
		self.Destroy()


class SectionList(wx.grid.GridTableBase):
	def __init__(self):
		wx.grid.GridTableBase.__init__(self)
		self.table = SectionAccessor().query_all_sections()
		self.attr_names = ["dname", "cno", "sectno", "pname"]
		self.column_labels = [u"开课院系", u"课程编号", u"开课编号", u"授课老师", u"课程名称"]
	
	def GetColLabelValue(self, col):
		return self.column_labels[col]
	
	def GetValue(self, row, col):
		if col == 4:
			return self.table[row].course.cname
		else:
			return getattr(self.table[row], self.attr_names[col])
	
	def GetNumberRows(self):
		return len(self.table)
	
	def GetNumberCols(self):
		return len(self.column_labels)
