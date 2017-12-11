# -*- coding:utf-8 -*-
from dao.DatabaseConnection import database
import traceback


class UserAccessor(object):
	"""
	用户登陆，数据库访问模块
	
	管理员：能够支持全部功能（查询所有学生基本信息，修改所有学生基本信息，查询学生选课信息，修改学生选课信息，删除某门课的全部信息）
	教师：能够支持部分功能（查询所有学生基本信息，查询学生选课信息，修改学生选课信息）
	学生：能够支持极少部分功能（查询所有学生基本信息）
	"""
	def __init__(self):
		pass
	
	def login(self, username, password) -> int:
		"""
		用户登陆
		:param username:用户名
		:param password:密码
		:return:-1为密码错误，-2为用户名不存在，0为管理员权限，1为教师权限，2为学生权限
		"""
		try:
			with database.cursor() as cursor:
				sql = r"SELECT password,auth FROM userinfo WHERE username=?"
				cursor.execute(sql, username)
				result = cursor.fetchall()
				if len(result) == 0 or len(result) != 1:
					return -2  # 用户名不存在
				elif result[0].password != password:
					return -1  # 密码错误
				else:
					return result[0].auth
		except Exception as e:
			traceback.print_exc()
			return -1
	
	def revise_password(self, username, password) -> int:
		"""
		修改用户密码
		:param username: 用户名
		:param password: 新密码
		:return: 0为失败，1为修改成功
		"""
		try:
			with database.cursor() as cursor:
				sql = "UPDATE userinfo SET password=? WHERE username=?"
				result = cursor.execute(sql, password, username)
				return result.rowcount
		except Exception as e:
			traceback.print_exc()
			return 0


if __name__ == '__main__':
	ua = UserAccessor()
	# print(ua.login("admin", "123456"))
	# print(ua.login("teacher", "111"))
	# print(ua.login("student", "222"))
	# print(ua.login("zzz", "zzz"))
	# print(ua.login("admin", "zzz"))
	# print(ua.revise_password("student", "foo"))
