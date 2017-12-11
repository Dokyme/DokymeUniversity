import traceback
from vo.Student import Student
from vo.Major import Major
from dao.DatabaseConnection import database


class StudentAccessor(object):
	def __init__(self):
		pass
	
	def query_specified_student_major(self, sid) -> list:
		"""
		查询某个学生的主修专业
		:param sid:
		:return:
		"""
		major = list()
		try:
			with database.cursor() as cursor:
				sql = "SELECT m.dname,m.sid FROM major m WHERE m.sid={}".format(sid)
				for row in cursor.execute(sql):
					m = Major()
					m.sid = row[1]
					m.dname = row[0]
					major.append(m)
				return major
		except Exception as e:
			traceback.print_exc()
			return []
	
	def query_ambiguous_student_abstract_info(self, sname):
		"""
		
		:param sname:
		:return:
		"""
		result = []
		try:
			with database.cursor() as cursor:
				sql = "SELECT * FROM student WHERE sname LIKE ? "
				for row in cursor.execute(sql, "%{}%".format(sname)).fetchall():
					stu = Student()
					stu.sid = row[0]
					stu.sname = row[1]
					stu.sex = row[2]
					stu.age = row[3]
					stu.year = row[4]
					stu.gpa = row[5]
					result.append(stu)
			return result
		except Exception as e:
			traceback.print_exc()
			return []
	
	def query_specified_student_abstract_info(self, sid):
		"""
		
		:param sid:
		:return:
		"""
		try:
			with database.cursor() as cursor:
				sql = "SELECT * FROM student WHERE sid={}".format(sid)
				cursor.execute(sql)
				row = cursor.fetchall()
				if len(row) == 0:
					return None
				row = row[0]
				stu = Student()
				stu.sid = row[0]
				stu.sname = row[1]
				stu.sex = row[2]
				stu.age = row[3]
				stu.year = row[4]
				stu.gpa = row[5]
				return stu
		except Exception as e:
			traceback.print_exc()
			return None
	
	def query_all_student_abstract_info(self):
		"""
		查询所有学生的基本信息
		:return:
		"""
		result = []
		try:
			with database.cursor() as cursor:
				sql = "SELECT * FROM student"
				for row in cursor.execute(sql):
					stu = Student()
					stu.sid = row[0]
					stu.sname = row[1]
					stu.sex = row[2]
					stu.age = row[3]
					stu.year = row[4]
					stu.gpa = row[5]
					result.append(stu)
			return result
		except Exception as e:
			traceback.print_exc()
			return None
	
	def update_specified_student_info(self, sid, field, value):
		"""
		更新某个学生的基本信息
		:param sid:
		:param field:
		:param value:
		:return:
		"""
		try:
			with database.cursor() as cursor:
				sql = "UPDATE student SET {}=? WHERE sid=?".format(field)
				result = cursor.execute(sql, value, sid)
				return result.rowcount
		except Exception as e:
			traceback.print_exc()
			return 0
	
	def delete_specified_student(self, sid):
		"""
		删除某个学生的全部信息（级联）
		:param sid:
		:return:
		"""
		try:
			with database.cursor() as cursor:
				sql = "DELETE FROM student WHERE sid=?"
				result = cursor.execute(sql, sid)
				return result.rowcount
		except Exception as e:
			traceback.print_exc()
			return 0


if __name__ == '__main__':
	sa = StudentAccessor()
	# print(sa.query_all_student_abstract_info())
	# for major in sa.query_specified_student_major(1):
	# 	print(major)
	# sa.update_specified_student_info(1, "sex", "m")
	# print(sa.delete_specified_student(1))
	sa.query_ambiguous_student_abstract_info("Pi")
