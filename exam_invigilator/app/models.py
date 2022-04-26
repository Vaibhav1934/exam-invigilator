

# Create your models here.
import datetime
from django.db import models
from django.db.models import Model 
from .user_app import * 


class dept(models.Model):

                  depts=models.CharField(primary_key=True,max_length=50,default='none')
                  
    
class faculty(models.Model):
	fname=models.CharField(max_length=50,null=False,default='')
	password=models.CharField(max_length=50,null=False,default="123")
	save_user(fname,password)

class room(models.Model):
	roomno=models.IntegerField(primary_key=True)
	
	
class exam(models.Model):
	exam_date=models.DateField()
	exam_time=models.CharField(max_length=50,default='9:30-12:30')
	ses=(('M',"Morning"),('A','Afternoon'))
	session=models.CharField(max_length=10,choices=ses,default='M')	
	subject=models.CharField(max_length=50)
	room=models.ForeignKey(room, on_delete=models.CASCADE)


class exam_inv(models.Model):
		    
                   id=models.AutoField(primary_key=True)
                   
                   fname=models.CharField(max_length=50,null=False,default='')
                   froom=models.IntegerField(default=' ')
                   session=models.CharField(max_length=10,default='M')
                   exam_date=models.DateField(default=str(datetime.date.today()))

class head(models.Model):
	heading=models.CharField(max_length=1000,default='EXAM TIMETABLE')

	





