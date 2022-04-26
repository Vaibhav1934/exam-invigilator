from django.db import connection


cursor = connection.cursor()

def filter_data(exam_date):

	cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and b.session =a.session ) and a.exam_date ='{exam_date}';" )
	
	return cursor.fetchall()
	
     #pass

     
def ex_date():

	cursor.execute( "select exam_date from app_exam limit 1 ;")
	return cursor.fetchall()[0][0]
     
     
