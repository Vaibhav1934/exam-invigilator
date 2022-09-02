from django.db import connection


cursor = connection.cursor()

def filter_data_new(exam_date):

	cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session ,a.id from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and a.session =b.session and b.froom=a.room_id ) and a.exam_date ='{exam_date}' ;" )
	#Sprint(cursor.fetchall())
	return cursor.fetchall()
	
     #pass
def room_1(exam_date):

	#cursor.execute(f"select a.room_id from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and b.froom=a.room_id ) and a.exam_date ='{exam_date}' ;" )
	#Sprint(cursor.fetchall())
	
	cursor.execute(f"select a.room_id,count(*) from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date  ) and a.exam_date ='{exam_date}' group by a.room_id having count(*) ;" )

	return cursor.fetchall()
    
def ses_1(exam_date,room):
    
     	#cursor.execute(f"select a.session from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and a.session and b.froom=a.room_id ) and a.exam_date ='{exam_date}' and a.room_id='{room}' ;" )
     	
     	cursor.execute(f"select a.session from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date  and b.froom=a.room_id and b.session=a.session ) and a.exam_date ='{exam_date}' and a.room_id='{room}';")

     	
     	return cursor.fetchall()

def del_exam():

	cursor.execute(f"delete from app_exam;" )
	return cursor.fetchall()

		
def fname_no_in_exam():

		cursor.execute(f"select a.fname ,a.inv_or_dc,a.id from app_faculty a where   not exists ( select b.fname from  app_exam_inv  b where b.fname = a.fname ) ;" )
		return cursor.fetchall()


     
def new():

	#cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session ,a.id from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and a.session =b.session and b.froom=a.room_id )  ;" )
	#Sprint(cursor.fetchall())
	cursor.execute(f"select a.exam_date from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date ) group by a.exam_date having count(a.exam_date)>1  ;" )
	return cursor.fetchall()
def new1(r):

	cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session ,a.id from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and a.session =b.session and b.froom=a.room_id ) and a.session='{r}' ;" )
	#Sprint(cursor.fetchall())
	return cursor.fetchall()	


def filter_data(exam_date,ses):

	cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session ,a.id from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and a.session =b.session and b.froom=a.room_id ) and a.exam_date ='{exam_date}' and a.session='{ses}';" )
	#Sprint(cursor.fetchall())
	print(ses,";;;;;;;;;;;;;;;;;;")
	return cursor.fetchall()
	
     #pass

     
def ex_date():

	cursor.execute( "select exam_date from app_exam limit 1 ;")
	return cursor.fetchall()[0][0]


def filter_data_inv(exam_date): 
	 cursor.execute(f"select a.exam_date,a.subject,a.room_id,a.session, a.id from app_exam a where   not exists ( select b.exam_date from  app_exam_inv  b where b.exam_date = a.exam_date and  b.froom=a.room_id ) and a.exam_date ='{exam_date}';")
	 return cursor.fetchall()
	 
	 
def  session_g(exam_date,sub,room):
	 print(exam_date,sub,room)	 
	 cursor.execute(f"select a.session from app_exam a where room_id='{room}' and subject='{sub}' and exam_date='{exam_date}';")
	 print(cursor.fetchall())
	 return cursor.fetchall()
	 
	 
def  count_s(exam_date,fname):	 
	 cursor.execute(f"select count(session) from app_exam_inv where fname='{fname}' and exam_date='{exam_date}';")
	 return cursor.fetchall()	 
	
def delt():

	 cursor.execute("delete from app_exam_inv ;")
	 print(cursor.fetchall())
	 return cursor.fetchall()
	 
def print_al():
	
		cursor.execute("select e.exam_date,e.fname,e.session from app_exam_inv e, app_faculty f where  e.fname=f.fname order by exam_date;")
		return cursor.fetchall()

def printinv():
	
	cursor.execute("select e.exam_date,e.fname,e.session from app_exam_inv e, app_faculty f where  e.fname=f.fname and inv_or_dc='invigilator' order by exam_date;")
	
	
	return cursor.fetchall()
	
def printdc():
	
	cursor.execute("select e.exam_date,e.fname,e.session from app_exam_inv e, app_faculty f where  e.fname=f.fname and inv_or_dc='dc' order by exam_date;")
	
	return cursor.fetchall()

def Delete_all_fac():
		
		cursor.execute("delete from app_faculty;")
		return cursor.fetchall()	
def del_room():

		cursor.execute("delete from app_room;")
		return cursor.fetchall()	
def all_fac_is_staf():

		cursor.execute("delete from auth_user where is_staff=0;")
		return cursor.fetchall()


def delete_user(id):
		cursor.execute(f"delete from auth_user where is_staff=0 and username='{id}';")
		return cursor.fetchall()

def inv_true(val):

	inv_or_dc=cursor.execute(f"select inv_or_dc from app_faculty where fname='val';")
	if inv_or_dc=="dc":
		return False
	else:
		return True
	
def out(name,date):	
	cursor.execute(f"select count(e.fname) from app_exam_inv e, app_faculty f where e.exam_date='{date}' and e.fname='{name}' and f.inv_or_dc='dc' and  e.session='M' ;")
	mon=cursor.fetchall()[0][0]
	cursor.execute(f"select count(e.fname) from app_exam_inv e, app_faculty f where e.exam_date='{date}' and e.fname='{name}' and f.inv_or_dc='dc' and  e.session='A' ;")
	af=cursor.fetchall()[0][0]
	print(mon,af,".................")
	if int(mon)>0 and int(af)==0  :
		print('mon')
		return 'mon'
	elif int(af)>0 and int(mon)==0 :
		print('af')
		return 'af'
	elif int(af)==1 and int(mon)==1:
	 
		return 'all'
	
	else:
		print('all')
		return True
