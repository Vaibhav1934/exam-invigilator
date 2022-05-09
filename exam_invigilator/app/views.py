from logging import exception
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth,messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout as get_out
import django.contrib.auth 
from exam_invigilator import settings
from django.core.mail import send_mail,EmailMessage
from django.db.models import Count
from django.http import HttpResponse,HttpResponseRedirect
from .models import faculty,room,exam,dept,exam_inv
from .cal import format_mon
import os,datetime
from .word_op import*
from .user_app import * 
from django.contrib.auth.decorators import login_required
from .sql_query import *
# Create your views here.




def login(request):
	

     	
     return  render (request,'index.html')
        
def signin(request):



	if request.method=='POST':
	
		print(request.POST['loginUser'],request.POST['loginPassword'])	
		
		user = auth(request.POST['loginUser'],request.POST['loginPassword'])
	
		try:	
			
			if user is not None:
				
				django.contrib.auth.login(request,user)
				
				if user.is_superuser:
				
					return redirect(admin_home)
				else:	
				       
					return redirect(fac_home)
	
			else:
			
				messages.error(request,'Invalid cerdentials!')
				return render(request,'index.html')
			
			
		except Exception as e:
		
			 print(e, " login didnt work")
		 
	
	else:
		
		
		return render(request,'index.html')















@login_required()


def exam_duties(request):

		         
			def record_duties():
			
			       pass
			dates=exam.objects.values('exam_date').annotate(count=Count('exam_date')).filter(count__gt=0)
			nameofcurrentuser=request.user.username
			print(nameofcurrentuser)
			inv_or_dc=faculty.objects.filter(fname=nameofcurrentuser)
			for i in inv_or_dc:
				inv_or_dc=i.inv_or_dc
			
			
			
			if request.GET.get('submit'):
				if request.method=='GET':
				
					print(format_mon(request.GET['submit']))
					mypkt=request.GET['submit']
					global exam_date
					exam_date= str(format_mon(mypkt))
					if inv_or_dc=='invigilator':
						data=filter_data_inv(exam_date)
					elif  inv_or_dc=='dc':
							data=filter_data(exam_date)
					
			
			else:
		        
				
				
				#exam_date=ex_date()
				pass
						
			try:	
			
			
				
		
				print(exam_date,type(exam_date))
			
			
				if inv_or_dc=='invigilator':
						data=filter_data_inv(exam_date)
				elif  inv_or_dc=='dc':
							data=filter_data(exam_date)
			
			

			
		
	
				#print(exam_date,'date')
				print(data)
			
				
  
	
			
			
				content_mor=exam_inv.objects.filter(fname=nameofcurrentuser,exam_date= exam_date,session='M')
				content_af=exam_inv.objects.filter(fname=nameofcurrentuser,exam_date= exam_date,session='A')

			
				lc=[]
				af=[]     

			
				dates=exam.objects.values('exam_date').annotate(count=Count('exam_date')).filter(count__gt=0)


			
				try:   
					if request.GET.get('sub_inv_2'):
					   print(request.GET['radioaf_inv'],'yes')
					   ex=exam_inv(fname=nameofcurrentuser,froom=request.GET['radioaf_inv'],session=session_g(format_mon(request.GET['dates']),request.GET['subject'],request.GET['radioaf_inv'])[0][0],exam_date=exam_date)
					   ex.save()	
					   return redirect(exam_duties)   

				except  Exception as e:
			
					print(e,' sub_invi_2 didnt work properly')			
						
				try:
					if request.GET.get('sub1'):
					
					   print(request.GET['radiomn'],'yes')
					   
					   
			   	
					   ex= exam_inv(fname=nameofcurrentuser,froom=request.GET['radiomn'],session='M',exam_date=exam_date)
					   ex.save()
					   print(ex)
					   return  redirect(exam_duties) 
		
				except Exception as e:
				
				
						print(e ,'sub 1 didnt work properly')
			
				try:   
					if request.GET.get('sub2'):
					   print(request.GET['radioaf'],'yes')
					   print(exam_date)
					   ex= exam_inv(fname=nameofcurrentuser,froom=request.GET['radioaf'],session='A',exam_date=exam_date)
					   ex.save()	
					   return redirect(exam_duties)   

				except  Exception as e:
			
					print(e,'sub2 didnt work properly')
			
			
			

				c=[]
				for i in data:
					print(data)

			
				return render(request,'faculty.html',{'data':data,'nameofcurrentuser':nameofcurrentuser, 'dates':dates,'lc':content_mor,'af':content_af,'inv_or_dc':inv_or_dc})                
              
			except:
		
				return render(request,'faculty.html',{'nameofcurrentuser':nameofcurrentuser, 'dates':dates,'inv_or_dc':inv_or_dc})           

                 
@login_required()              
def fac_home(request):


                 
                 nameofcurrentuser=request.user.username
                 content =exam_inv.objects.filter(fname=nameofcurrentuser)
                 for con in content:
                      print(con.froom,con.exam_date,con.session)
                 return render(request,'home_fac.html',{'content':content,'nameofcurrentuser':nameofcurrentuser})                   



def admin_home(request):

		data=exam_inv.objects.values('exam_date','fname','froom').annotate(count=Count('exam_date')).filter(count__gt=0)
		

		
		#for d in data:
			#print(d)
		print("1......")
		if request.method=='GET':
			print("2...")
			if request.GET.get('Delete') :
				print("4......")
				exam_date=format_mon(request.GET.get('Delete'))
				
				froom=request.GET.get('froom')
				fname=request.GET.get('fname')
				print(exam_date,froom,fname)
				delt(exam_date,froom,fname)
		
		

		return render(request,'admin.html',{'data':data})

	

def admin_fac(request):

	if request.method=='GET':
		if request.GET.get('un') and request.GET.get('pw'):
			fname=request.GET.get('un')
			password=request.GET.get('pw')
			fac= faculty(fname=fname,password=password)
			fac.save()
			save_user(fname,password)
		
			#print(request.GET['un'],request.GET['pw'])
	
		data=faculty.objects.all()
		return render(request,'admin_fac.html',{'data':data})
	
		pass



def admin_room(request):

	if request.method=='GET':
		if request.GET.get('rm') :
			rm= room(roomno=request.GET.get('rm'))
			rm.save()
		data=room.objects.all()
		return render(request,'admin_room.html',{'data':data})
	



def admin_exam(request):

	if request.method=='GET':
		if request.GET.get('date') and request.GET.get('es') and request.GET.get('ss') and request.GET.get('rm'):
		
			ex= exam(exam_date=request.GET.get('date'),subject=request.GET.get('es'),session=request.GET.get('ss'),room_id=request.GET.get('rm'))
			ex.save()
	
	
		data=room.objects.all()
		exams=exam.objects.all()
		for i in data:
				print(i.roomno)
		return render(request,'admin_exam.html',{'data':data,'exams':exams})
		pass
		


                 
                 
            
                 
                
def logout(request):
                
                 get_out(request)
                 return  redirect (login)
                 

