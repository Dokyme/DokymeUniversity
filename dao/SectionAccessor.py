from dao.DatabaseConnection import database
from vo.Section import Section
from vo.Course import Course
import traceback


class SectionAccessor(object):
	def __init__(self):
		pass
	
	def delete_specifide_section(self, section):
		"""
		删除某门课的所有信息（级联）
		:param section:
		:return:
		"""
		try:
			with database.cursor() as cursor:
				sql = "DELETE FROM section WHERE dname=? and cno=? and sectno=?"
				result = cursor.execute(sql, section.dname, section.cno, section.sectno)
				return result.rowcount
		except Exception as e:
			traceback.print_exc()
			return 0
	
	def query_all_sections(self) -> list:
		"""
		查询所有开的课程
		:return:
		"""
		try:
			sections = list()
			with database.cursor() as cursor:
				sql = "SELECT s.sectno,s.dname,s.cno,c.cname,s.pname FROM section s,course c WHERE s.dname=c.dname AND s.cno=c.cno"
				for row in cursor.execute(sql):
					c = Course()
					s = Section()
					s.sectno = row[0]
					s.dname = row[1]
					s.cno = row[2]
					s.pname = row[4]
					c.cname = row[3]
					s.course = c
					sections.append(s)
				return sections
		except Exception as e:
			traceback.print_exc()
			return None


if __name__ == '__main__':
	sa = SectionAccessor()
	print(sa.query_all_sections())
