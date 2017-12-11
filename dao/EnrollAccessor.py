from vo.Enroll import Enroll
from vo.Section import Section
from vo.Course import Course
import traceback

from dao.DatabaseConnection import database


class EnrollAccessor(object):
	def __init__(self):
		pass
	
	def delete_enroll_of_specified_student(self, sid, grade, enroll) -> int:
		"""
		删除某个学生的某门选课
		:param sid:
		:param grade:
		:param enroll:
		:return:
		"""
		try:
			with database.cursor() as cursor:
				sql = "DELETE FROM enroll WHERE sid=? AND grade=? AND dname=? AND cno=? AND sectno=?"
				result = cursor.execute(sql, sid, grade, enroll.dname, enroll.cno, enroll.sectno)
				return result.rowcount
		except Exception as e:
			traceback.print_exc()
			return 0
	
	def add_enroll_to_specified_student(self, sid, grade, section) -> int:
		"""
		添加某个学生的某门选课
		:param sid:
		:param grade:
		:param section:
		:return:
		"""
		try:
			with database.cursor() as cursor:
				sql = "INSERT INTO enroll (sid,grade,dname,cno,sectno)VALUES(?,?,?,?,?)"
				result = cursor.execute(sql, sid, grade, section.dname, section.cno, section.sectno)
				return result.rowcount
		except Exception as e:
			traceback.print_exc()
			return 0
	
	def query_specified_student_enrolls(self, sid) -> list:
		"""
		查询某个学生的所选的所有课
		:param sid:
		:return:
		"""
		try:
			enrolls = set()
			with database.cursor() as cursor:
				sql = "SELECT stu.sid,stu.sname,stu.sex,stu.age,stu.year,stu.gpa,m.dname,e.dname,e.cno,e.sectno,e.grade,s.pname,c.cname,c.dname " \
				      "FROM student stu,enroll e,section s,course c,major m " \
				      "WHERE stu.sid=m.sid AND stu.sid=e.sid AND e.dname=s.dname AND e.cno=s.cno AND e.sectno=s.sectno AND s.dname=c.dname AND s.cno=c.cno AND stu.sid=" + str(
					sid)
				result_set = cursor.execute(sql)
				for row in result_set:
					c = Course()
					c.cname = row[13]
					sect = Section()
					sect.pname = row[11]
					e = Enroll()
					e.dname = row[7]
					e.cno = row[8]
					e.sectno = row[9]
					e.grade = row[10]
					e.section = sect
					sect.course = c
					enrolls.add(e)
				return list(enrolls)
		except Exception as e:
			traceback.print_exc()
			return []


if __name__ == '__main__':
	ea = EnrollAccessor()
# print(ea.query_specified_student_enrolls(1))
# print(ea.query_specified_student_enrolls(2))
# print(ea.query_specified_student_enrolls(3))
