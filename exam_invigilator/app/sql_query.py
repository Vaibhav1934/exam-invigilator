from django.db import connection


cursor = connection.cursor()

def filter_data(exam_date):

	cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and b.session =a.session ) and a.exam_date ='{exam_date}';" )
	
	return cursor.fetchall()
	
     #pass

     
def ex_date():

	cursor.execute( "select exam_date from app_exam limit 1 ;")
	return cursor.fetchall()[0][0]


def filter_data_inv(exam_date): 
	 cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date ) and a.exam_date ='{exam_date}';")
	 return cursor.fetchall()
	 
	 
def  session_g(exam_date,sub,room):	 
	 cursor.execute(f"select a.session from app_exam a where room_id='{room}' and subject='{sub}' and exam_date='{exam_date}';")
	 return cursor.fetchall()
	 
	 
def  count_s(exam_date,fname):	 
	 cursor.execute(f"select count(session) from app_exam_inv where fname='{fname}' and exam_date='{exam_date}';")
	 return cursor.fetchall()	 
	
def delt(exam_date,froom,fname):

	 cursor.execute(f"delete from app_exam_inv where fname='{fname}' and exam_date='{exam_date}' and froom='{froom}';")
