# -*- coding:utf-8 -*-
import wx
import wx.grid

from dao.StudentAccessor import StudentAccessor
from dao.EnrollAccessor import EnrollAccessor


class StudentListWindow(wx.Frame):
	def __init__(self, parent, data, app):
		wx.Frame.__init__(self, None,
		                  title=u"学生信息列表",
		                  pos=wx.DefaultPosition,
		                  size=wx.Size(850, 900),
		                  style=wx.DEFAULT_FRAME_STYLE)
		self.app = app
		self.parent = parent
		self.data = data
		self.enroll_accessor = EnrollAccessor()
		self.student_accessor = StudentAccessor()
		self.btn_confirm_revise = None
		self.btn_add_enroll = None
		self.btn_delete_enroll = None
		self.input_sname_value = None
		self.input_sid_value = None
		self.input_age_value = None
		self.input_sex_value = None
		self.input_year_value = None
		self.input_gpa_value = None
		self.student_grid = None
		self.enroll_grid = None
		self.major_grid = None
		self.major_list = None
		self.enroll_list = None
		self.student_list = None
		self.input_search_sid = None
		self.input_search_sname = None
		self.btn_search_sid = None
		self.btn_search_sname = None
		self.btn_edit_student_info = None
		self.btn_refresh = None
		self.btn_delete_student_info = None
		self.__init_widgets()
		self.__init_events()
	
	def __init_events(self):
		"""
		
		:return:
		"""
		self.Bind(wx.EVT_BUTTON, self.__search_sid, self.btn_search_sid)
		self.Bind(wx.EVT_BUTTON, self.__search_sname, self.btn_search_sname)
		self.Bind(wx.EVT_TEXT, self.__search_sname, self.input_search_sname)
		self.Bind(wx.EVT_BUTTON, self.__delete_student, self.btn_delete_student_info)
		self.Bind(wx.EVT_BUTTON, self.__refresh, self.btn_refresh)
		self.Bind(wx.EVT_BUTTON, self.__delete_enroll, self.btn_delete_enroll)
		self.Bind(wx.EVT_BUTTON, self.__add_enroll, self.btn_add_enroll)
		self.student_grid.Bind(wx.grid.EVT_GRID_CMD_CELL_LEFT_CLICK, self._search_full_info)
	
	def __add_enroll(self, event):
		"""
		
		:param event:
		:return:
		"""
		data = {"sid": int(self.input_sid_value.GetValue())}
		self.app.jump_to_add_enroll_window(self, data)
	
	def __delete_enroll(self, event):
		"""
		
		:param event:
		:return:
		"""
		rows = self.enroll_grid.GetSelectedRows()
		if len(rows) == 0:
			wx.MessageDialog(self, u"你尚未选择任何选课！", style=wx.ICON_ERROR | wx.OK).ShowModal()
		else:
			row = rows[0]
			enroll = self.enroll_list.table[row]
			sid = int(self.input_sid_value.GetValue())
			result = self.enroll_accessor.delete_enroll_of_specified_student(sid, enroll.grade, enroll)
			if result == 1:
				wx.MessageDialog(self, u"删除选课成功~", style=wx.ICON_INFORMATION | wx.OK).ShowModal()
			else:
				wx.MessageDialog(self, u"删除选课失败！", style=wx.ICON_ERROR | wx.OK).ShowModal()
			self._search_full_info(None)
	
	def __confirm_info_update(self, event):
		"""
		
		:param event:
		:return:
		"""
		r1 = self.__update_if_dirty("sid", self.input_sid_value)
		r2 = self.__update_if_dirty("age", self.input_age_value)
		r3 = self.__update_if_dirty("year", self.input_year_value)
		r4 = self.__update_if_dirty("sex", self.input_sex_value)
		r5 = self.__update_if_dirty("gpa", self.input_gpa_value)
		r6 = self.__update_if_dirty("sname", self.input_sname_value)
		if r1 * r2 * r3 * r4 * r5 * r6 == 1:
			wx.MessageDialog(self, message=u"信息更新成功~", style=wx.ICON_INFORMATION | wx.OK).ShowModal()
		else:
			wx.MessageDialog(self, message=u"信息更新失败！", style=wx.ICON_ERROR | wx.OK).ShowModal()
	
	def _search_full_info(self, event):
		"""
		
		:return:
		"""
		if not event:
			student = self.student_list.table[self.student_grid.GetSelectedRows()[0]]
		else:
			student = self.student_list.table[event.GetRow()]
		sid = student.sid
		self.input_sid_value.SetValue(str(sid))
		self.input_sname_value.SetValue(student.sname)
		self.input_age_value.SetValue(str(student.age))
		self.input_gpa_value.SetValue(str(student.gpa))
		self.input_sex_value.SetValue(student.sex)
		self.input_year_value.SetValue(str(student.year))
		majors = self.student_accessor.query_specified_student_major(sid)
		enrolls = self.enroll_accessor.query_specified_student_enrolls(sid)
		self.major_list.table = majors
		self.enroll_list.table = enrolls
		self.major_grid.ForceRefresh()
		self.enroll_grid.ForceRefresh()
		if event:
			event.Skip()
	
	def __refresh(self, event):
		"""
		
		:param event:
		:return:
		"""
		result = self.student_accessor.query_all_student_abstract_info()
		self.student_list.table = result
		self.student_grid.ForceRefresh()
		self.student_grid.GoToCell(0, 0)
	
	def __delete_student(self, event):
		"""
		
		:param event:
		:return:
		"""
		row = self.student_grid.GetSelectedRows()[0]
		student = self.student_list.table[row]
		result = self.student_accessor.delete_specified_student(student.sid)
		if result != 0:
			wx.MessageDialog(self, message=u"删除学生信息成功~", style=wx.ICON_INFORMATION | wx.OK).ShowModal()
		else:
			wx.MessageDialog(self, message=u"删除学生信息失败!", style=wx.ICON_ERROR | wx.OK).ShowModal()
	
	def __search_sid(self, event):
		"""
		根据sid进行精确搜索的回调函数，由button事件触发。
		:param event:
		:return:
		"""
		sid = self.input_search_sid.GetValue()
		if sid == "":
			result = self.student_accessor.query_all_student_abstract_info()
			self.student_list.table = result
		else:
			result = self.student_accessor.query_specified_student_abstract_info(sid)
			if not result:
				self.student_list.table = []
			else:
				self.student_list.table = [result]
			self.student_grid.ForceRefresh()
			self.student_grid.GoToCell(row=0, col=1)
	
	def __search_sname(self, event):
		"""
		根据sname的部分内容进行模糊搜索的回调函数，由input的内容变更事件或button事件触发。
		:param event:
		:return:
		"""
		sname = self.input_search_sname.GetValue()
		if sname == "":
			result = self.student_accessor.query_all_student_abstract_info()
		else:
			result = self.student_accessor.query_ambiguous_student_abstract_info(sname)
		self.student_list.table = result
		self.student_grid.ForceRefresh()
		self.student_grid.GoToCell(row=0, col=1)
	
	def __init_widgets(self):
		"""
		
		:return:
		"""
		panel = wx.Panel(self)
		panel.SetBackgroundColour("#FFFFFF")
		layout = wx.BoxSizer(wx.VERTICAL)
		group_top = wx.BoxSizer(wx.HORIZONTAL)
		group_middle = wx.BoxSizer(wx.HORIZONTAL)
		group_buttom = wx.BoxSizer(wx.HORIZONTAL)
		group_middle_right = wx.BoxSizer(wx.VERTICAL)
		self.__init_top_group(group_top, panel)
		self.__init_left_button_group(group_buttom, panel)
		self.__init_right_prompt(group_middle_right, panel)
		self.__init_right_grids(group_middle_right, panel)
		self.__init_left_grid(group_middle, panel)
		group_middle.Add(group_middle_right, 1, wx.EXPAND, 5)
		layout.Add(group_top, 0, wx.EXPAND, 5)
		layout.Add(group_middle, 0, wx.ALIGN_LEFT, 5)
		layout.Add(group_buttom, 0, wx.EXPAND, 5)
		panel.SetSizer(layout)
	
	def __init_top_group(self, group_top, panel):
		"""
		
		:param group_top:
		:param panel:
		:return:
		"""
		font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
		prompt_sid = wx.StaticText(panel, label=u"学号", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_sid.SetFont(font)
		prompt_sname = wx.StaticText(panel, label=u"姓名", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_sname.SetFont(font)
		self.input_search_sid = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_search_sname = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.btn_search_sid = wx.Button(panel, label=u"精确搜索")
		self.btn_search_sname = wx.Button(panel, label=u"模糊搜索")
		group_top.Add(prompt_sid, 0, wx.ALL, 5)
		group_top.Add(self.input_search_sid, 0, wx.ALL, 5)
		group_top.Add(self.btn_search_sid, 0, wx.ALL, 5)
		group_top.Add(prompt_sname, 0, wx.ALL, 5)
		group_top.Add(self.input_search_sname, 0, wx.ALL, 5)
		group_top.Add(self.btn_search_sname, 0, wx.ALL, 5)
	
	def __init_right_grids(self, group_middle_right, panel):
		"""
		
		:param group_middle_right:
		:param panel:
		:return:
		"""
		self.btn_delete_enroll = wx.Button(panel, label=u"删除")
		self.btn_add_enroll = wx.Button(panel, label=u"添加")
		self.major_list = MajorList()
		self.enroll_list = EnrollList()
		major_grid = CustomedGird(panel, 444, wx.DefaultPosition, wx.DefaultSize, 0)
		major_grid.init(self.major_list, min_size=wx.Size(400, 120), size=wx.Size(200, 50))
		major_grid.SetColSize(0, 400)
		enroll_grid = CustomedGird(panel, 555, wx.DefaultPosition, wx.DefaultSize, 0)
		enroll_grid.init(self.enroll_list, min_size=wx.Size(400, 150), size=wx.Size(300, 50),
		                 max_size=wx.Size(600, 150))
		self.enroll_grid = enroll_grid
		self.major_grid = major_grid
		for i in range(6):
			enroll_grid.SetColSize(i, 66)
		group_right_major_grid = wx.BoxSizer(wx.VERTICAL)
		group_right_major_grid.Add(major_grid, 0, wx.ALL, 5)
		group_right_enroll_grid = wx.BoxSizer(wx.VERTICAL)
		group_right_enroll_grid.Add(enroll_grid, 0, wx.ALL, 5)
		group_right_enroll_operator = wx.BoxSizer(wx.HORIZONTAL)
		group_right_enroll_operator.Add(self.btn_add_enroll, 0, wx.ALL, 5)
		group_right_enroll_operator.Add(self.btn_delete_enroll, 0, wx.ALL, 5)
		group_middle_right.Add(group_right_major_grid, 0, wx.ALL, 5)
		group_middle_right.Add(group_right_enroll_grid, 0, wx.ALL, 5)
		group_middle_right.Add(group_right_enroll_operator, 0, wx.ALL, 5)
	
	def __init_right_prompt(self, group_middle_right, panel):
		"""
		
		:param group_middle_right:
		:param panel:
		:return:
		"""
		self.btn_confirm_revise = wx.Button(panel, label=u"确认修改")
		prompt_sname = wx.StaticText(panel, label=u"姓名", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_sid = wx.StaticText(panel, label=u"学号", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_age = wx.StaticText(panel, label=u"年龄", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_sex = wx.StaticText(panel, label=u"性别", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_year = wx.StaticText(panel, label=u"年级", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		prompt_gpa = wx.StaticText(panel, label=u"GPA", style=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		self.input_sname_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_sid_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_age_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_sex_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_year_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
		self.input_gpa_value = wx.TextCtrl(panel, style=wx.TE_LEFT)
		group_sid = wx.BoxSizer(wx.HORIZONTAL)
		group_sname = wx.BoxSizer(wx.HORIZONTAL)
		group_age = wx.BoxSizer(wx.HORIZONTAL)
		group_sex = wx.BoxSizer(wx.HORIZONTAL)
		group_year = wx.BoxSizer(wx.HORIZONTAL)
		group_gpa = wx.BoxSizer(wx.HORIZONTAL)
		group_sid.Add(prompt_sid, 0, wx.ALL, 5)
		group_sid.Add(self.input_sid_value, 0, wx.ALL, 5)
		group_sname.Add(prompt_sname, 0, wx.ALL, 5)
		group_sname.Add(self.input_sname_value, 0, wx.ALL, 5)
		group_age.Add(prompt_age, 0, wx.ALL, 5)
		group_age.Add(self.input_age_value, 0, wx.ALL, 5)
		group_sex.Add(prompt_sex, 0, wx.ALL, 5)
		group_sex.Add(self.input_sex_value, 0, wx.ALL, 5)
		group_year.Add(prompt_year, 0, wx.ALL, 5)
		group_year.Add(self.input_year_value, 0, wx.ALL, 5)
		group_gpa.Add(prompt_gpa, 0, wx.ALL, 5)
		group_gpa.Add(self.input_gpa_value, 0, wx.ALL, 5)
		group_middle_right.Add(group_sid, 0, wx.ALL, 5)
		group_middle_right.Add(group_sname, 0, wx.ALL, 5)
		group_middle_right.Add(group_age, 0, wx.ALL, 5)
		group_middle_right.Add(group_sex, 0, wx.ALL, 5)
		group_middle_right.Add(group_year, 0, wx.ALL, 5)
		group_middle_right.Add(group_gpa, 0, wx.ALL, 5)
		group_middle_right.Add(self.btn_confirm_revise, 0, wx.ALL, 5)
	
	def __init_left_grid(self, group_middle, panel):
		"""
		
		:param group_middle:
		:param panel:
		:return:
		"""
		group_middle_left = wx.BoxSizer(wx.VERTICAL)
		self.student_list = StudentList()
		self.student_grid = CustomedGird(panel, 333, wx.DefaultPosition, wx.DefaultSize, 0)
		self.student_grid.init(self.student_list, max_size=wx.Size(360, 500))
		group_middle_left.Add(self.student_grid, 0, wx.ALL, 5)
		group_middle.Add(group_middle_left, 1, wx.EXPAND, 5)
	
	def __init_left_button_group(self, group_buttom, panel):
		self.btn_refresh = wx.Button(panel, label=u"刷新")
		self.btn_delete_student_info = wx.Button(panel, label=u"删除")
		group_buttom.Add(self.btn_delete_student_info, 0, wx.ALL, 5)
		group_buttom.Add(self.btn_refresh, 0, wx.ALL, 5)
	
	def __update_if_dirty(self, attr, input_):
		"""
		
		:param attr:
		:param input_:
		:return:
		"""
		row = self.student_grid.GetSelectedRows()[0]
		if str(getattr(self.student_list.table[row], attr)) == input_.GetValue():
			return 1
		else:
			if attr == "gpa":
				new_value = float(input_.GetValue())
			elif attr == "sname":
				new_value = input_.GetValue()
			else:
				new_value = int(input_.GetValue())
			if self.student_accessor.update_specified_student_info(self.student_list.table[row].sid, attr,
			                                                       new_value) == 1:
				return 1
			else:
				return 0


class CustomedGird(wx.grid.Grid):
	def __init__(self, *args, **kwargs):
		wx.grid.Grid.__init__(self, *args, **kwargs)
	
	def init(self, table, takeOwnership=False, selmode=wx.grid.Grid.SelectRows, min_size=None, max_size=None,
	         size=None):
		super()._SetTable(table, takeOwnership, selmode)
		if min_size:
			self.SetMinSize(min_size)
		if max_size:
			self.SetMaxSize(max_size)
		if size:
			self.SetSize(size)
		self.DisableDragRowSize()
		self.SetMargins(0, 0)
		self.HideCellEditControl()
		self.DisableCellEditControl()
		self.AutoSizeColumns(True)
		self.SetSelectionMode(wx.grid.Grid.SelectRows)
		self.HideRowLabels()
	
	def GetColGridLinePen(self, col):
		return wx.Pen(wx.LIGHT_GREY, 1, wx.SOLID)


class EnrollList(wx.grid.GridTableBase):
	def __init__(self):
		wx.grid.GridTableBase.__init__(self)
		self.enroll_accessor = EnrollAccessor()
		self.table = []
		self.attr_name = ["dname", "cno", "sectno", "cname", "pname", "grade"]
		self.column_label = [u"开课院系", u"课程号", u"开课号", u"课程名称", u"教师名称", u"年级"]
	
	def GetColLabelValue(self, col):
		return self.column_label[col]
	
	def GetValue(self, row, col):
		if len(self.table) <= row:
			return ""
		if col < 3 or col == 5:
			return str(getattr(self.table[row], self.attr_name[col]))
		elif col == 3:
			return self.table[row].section.course.cname
		else:
			return self.table[row].section.pname
	
	def GetNumberRows(self):
		return 5
	
	def GetNumberCols(self):
		return len(self.column_label)
	
	def refresh(self, sid):
		result_set = self.enroll_accessor.query_specified_student_enrolls(sid)
		self.table = result_set


class MajorList(wx.grid.GridTableBase):
	def __init__(self):
		wx.grid.GridTableBase.__init__(self)
		self.student_accessor = StudentAccessor()
		self.attr_name = "dname"
		self.table = []
		self.column_label = u"主修专业"
	
	def GetColLabelValue(self, col):
		return self.column_label
	
	def GetValue(self, row, col):
		if len(self.table) <= row:
			return ""
		return str(getattr(self.table[row], "dname"))
	
	def GetNumberRows(self):
		return 3
	
	def GetNumberCols(self):
		return 1
	
	def refresh(self, sid):
		result_set = self.student_accessor.query_specified_student_major(sid)
		self.table = result_set


class StudentList(wx.grid.GridTableBase):
	def __init__(self):
		wx.grid.GridTableBase.__init__(self)
		self.table = StudentAccessor().query_all_student_abstract_info()
		self.column_labels = [u"学号", u"姓名", u"性别", u"年龄", u"年级", u"GPA"]
		self.attr_name = ["sid", "sname", "sex", "age", "year", "gpa"]
	
	def GetColLabelValue(self, col):
		return self.column_labels[col]
	
	def GetValue(self, row, col):
		if len(self.table) < 50 and len(self.table) <= row:
			return ""
		value = getattr(self.table[row], self.attr_name[col])
		if isinstance(value, float):
			return "{:.2}".format(value)
		return str(value)
	
	def GetNumberRows(self):
		if len(self.table) > 50:
			return len(self.table)
		else:
			return 50
	
	def GetNumberCols(self):
		return len(self.column_labels)
