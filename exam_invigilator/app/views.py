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
from django.http import HttpResponse 
from .models import faculty,room,exam,dept,exam_inv
from .cal import format_mon
import os,datetime
from .user_app import * 
from django.contrib.auth.decorators import login_required
from .sql_query import filter_data,ex_date
# Create your views here.



 
#exam_date=datetime.date.today()

#path=os.getcwd()




def login(request):
	
     #pass
     data=faculty.objects.all()
     for fac in data:
     	#print(fac.fname,"ffffffffffffffffffffffffffffff")
     	save_user(fac.fname,fac.password)
     	
     return  render (request,'index.html')
        
def signin(request):

          #if request.method=='POST':
                 
           #    username= request.POST['loginUser']
            #   password = request.POST['loginPassword']
               #global nameofcurrentuser
             #  nameofcurrentuser=username
              # print(nameofcurrentuser,password)
                 
               #try:
                #    data=faculty.objects.get(fname=username,password=password)
                 #   print(data)

                  #  if data:
                   # 	
                    #     return render(request,'home_fac.html',{'nameofcurrentuser':nameofcurrentuser})

               #except :
                #    print("!!!!!!!")
                 #   messages.error(request,'Invalid cerdentials!')
                  #  return render(request,'index.html')

	if request.method=='POST':
	
		print(request.POST['loginUser'],request.POST['loginPassword'])	
		
		user = auth(request.POST['loginUser'],request.POST['loginPassword'])	
		
		print("..............",user)
	
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
			
			if request.GET.get('submit'):
				if request.method=='GET':
					#print(request.GET['submit'],request.GET['submit'],request.GET['submit'])
					print(format_mon(request.GET['submit']))
					mypkt=request.GET['submit']
					global exam_date
					exam_date= str(format_mon(mypkt))
			
			else:
		        
				#exam_date=datetime.date.today()
				
				#exam_date=ex_date()
				pass
						
			try:	
				print('username = ',nameofcurrentuser)	
				print(exam_date,type(exam_date))
			
			
				#data=exam.objects.filter(exam_date= exam_date)
				data=filter_data(exam_date)
			
			

			
		
	
				print(exam_date,'date')
				print(data)
			
				for i in data:
					print(i)
  
				#ses=exam.objects.filter(exam_date= exam_date)
			
			
				content_mor=exam_inv.objects.filter(fname=nameofcurrentuser,exam_date= exam_date,session='M')
				content_af=exam_inv.objects.filter(fname=nameofcurrentuser,exam_date= exam_date,session='A')

			
				lc=[]
				af=[]     
				print( 'lc')
				for con in content_mor:
					lc.append(con.froom)
					print(lc)
				print(lc)
				print('lc') 
				
				for aft in content_af:
					af.append(aft.froom)
					print(af)
				print(af)
				print('af')
			
			
				dates=exam.objects.values('exam_date').annotate(count=Count('exam_date')).filter(count__gt=0)

			
						
				try:
					if request.GET.get('sub1'):
					
					   print(request.GET['radiomn'],'yes')
					   
					   print(exam_date," ............................................................................")
			   	
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
			
					print(e,' didnt work properly')
			
			
			

				c=[]
			#for i in ses:
			 #  c.append(i.session)
			#print(c)
			
				return render(request,'faculty.html',{'data':data,'nameofcurrentuser':nameofcurrentuser, 'dates':dates,'lc':content_mor,'af':content_af})                
              
			except:
		
				return render(request,'faculty.html',{'nameofcurrentuser':nameofcurrentuser, 'dates':dates})           
		#else:
              	#	return render(request,path+'/app/templates/html/faculty.html')
                 
@login_required()              
def fac_home(request):


                 
                 nameofcurrentuser=request.user.username
                 content =exam_inv.objects.filter(fname=nameofcurrentuser)
                 for con in content:
                      print(con.froom,con.exam_date,con.session)
                 return render(request,'home_fac.html',{'content':content,'nameofcurrentuser':nameofcurrentuser})                   



def admin_home(request):

		data=exam_inv.objects.all()
		
		
                   
		return render(request,'admin.html',{'data':data})

	

def admin_fac(request):

	print(request.GET.get('add'))
		#print(request.GET['un'],request.GET['pw'])


	return render(request,'admin_fac.html')

	pass



def admin_room(request):

	return render(request,'admin_room.html')
	pass



def admin_exam(request):


	return render(request,'admin_exam.html')
	pass
		


                 
                 
            
                 
                
def logout(request):
                
                 get_out(request)
                 return  redirect (login)
                 

