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
						if not exam_inv.objects.filter(fname=request.user.username,exam_date=exam_date):
							data=filter_data_inv(exam_date)
					elif  inv_or_dc=='dc':
						
						re=out(name=request.user.username,date=exam_date)
						print(re)
						if re=='mon':
						
							data=filter_data(exam_date,'A')
						elif re=='af':
							data=filter_data(exam_date,'M')
						elif re=='all':
							pass
						
						else:
							data=filter_data_new(exam_date)
							
					
			
			else:
		        
				
				
				#exam_date=ex_date()
				pass
						
			try:	
			
			
				
		
				print(exam_date,type(exam_date))
			
			
				if inv_or_dc=='invigilator':
					if not exam_inv.objects.filter(fname=request.user.username,exam_date=exam_date):
						data=filter_data_inv(exam_date)
				elif  inv_or_dc=='dc':
						re= out(name=request.user.username,date=exam_date)
						print(re)
						if re=='mon':
							data=filter_data(exam_date,'A')
						elif re=='af':
							data=filter_data(exam_date,'M')
						elif re=='all':
							pass
						else:
							data=filter_data_new(exam_date)

			
		
	
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
					   session=exam.objects.get(id=request.GET['radioaf_inv'])
					   froom=exam.objects.get(id=request.GET['radioaf_inv'])
					   print(request.GET['id'])
					   
					   print(session.session,"printing sesson")
					   print(froom)
					   froom=froom.room_id
					   print(froom,"sesession ......")
					   ex=exam_inv(fname=nameofcurrentuser,froom=froom,session=session.session,exam_date=exam_date)
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
				#for i in data:
				#	print(data)

			
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
	
			
		#return render(request,'edit.html')
		#pass
	
		#data=exam_inv.objects.values('exam_date','fname','froom').annotate(count=Count('exam_date')).filter(count__gt=0)
	data=exam_inv.objects.all()	
	faculty1=faculty.objects.all()
	room1=room.objects.all()
	#exam1=exam.objects.values('exam_date').annotate(count=Count('exam_date')).filter(count__gt=0)
	#print(exam1)
	#for i in exam1:
	#	print(i)
			
	if 1:
	#try:

		#for d in data:
			#print(d)
		print("1......")
		if request.method=='GET':
			#print("2...")
			if request.GET.get('Delete') :
				print("4......")
				#exam_date=format_mon(request.GET.get('exam_date'))
				
				#froom=request.GET.get('froom')
				#fname=request.GET.get('fname')
				#print(exam_date,froom,fname)
				id=request.GET.get('Delete')
				e=exam_inv.objects.get(id=id)
				e.delete()
				#delt(exam_date,froom,fname)
			if request.GET.get('edit'):
				id=request.GET.get('edit')
				#edit(request.GET.get('edit'))
				valu=exam_inv.objects.filter(id=id)
				val=[]
				inv=False
				dc=False
				for ro in valu:
					val.append(ro.fname)
					val.append(ro.exam_date)
					val.append(ro.froom)
					val.append(ro.session)	
					print(val)
				if inv_true(val[0])==True:
					
					inv=True
				else:
					dc=True
				
				if inv:
					r=exam_inv.objects.filter(fname=val[0],exam_date=val[1])
					for i in r:
					
						r=i.session
					
					print(r,"[]]]]]]]]]]")
					exam1=new1(r)
				if  dc:
					exam1=new()	



				print(exam1)
				return render(request,'edit.html',{'val':val,'id':id,'data':data,'faculty1':faculty1,'room1':room1,'exam1':exam1,'id':id})
			#date=request.GET.get("date")
			#print(date)
			if  request.GET.get('done1'):
					print("seeeleted")
					date=[]
					id=request.GET.get("id")
					date.append(request.GET.get("name"))
					date.append(format_mon(request.GET.get("date")))
					print(date)
					room1=room_1(exam_date=date[1])
					for room3 in room1:
						print(room3) 
					return render(request,'edit.html',{'room1':room1,'val':date,'sep':'1','id':id})
			if  request.GET.get('done2'):
					print("seeeleted")
					date=[]
					id=request.GET.get("id")
					date.append(request.GET.get("name"))
					date.append(request.GET.get("date"))
					date.append(request.GET.get("room"))
					print(date)
					ses=ses_1(date[1],date[2])
					print(ses[0])
					
					if len(ses)>1:
						ses='MN'

					return render(request,'edit.html',{'val':date,'sep':'1' , 'nov':'1','ses':ses,'id':id})								
					
			

			
				#d#ate1=format_mon(request.GET.get("date"))
				#print(date,"///////////////////")
					#print(exam1)
					#return render(request,'edit.html',{'val':val,'id':id,'data':data,'faculty1':faculty1,'room1':room1,'exam1':exam1})
			if request.GET.get('done'):
				id=request.GET.get("id")
				print(id,";;;;;;;;;;;;;;;;;;;;;;;;")
				session1=request.GET.get("session")
				room1=request.GET.get("room")
				date1=str(request.GET.get("date"))
				print(date1)
				name1=request.GET.get("name")
				print(date1)
				done=exam_inv.objects.filter(id=id)
				done.update(session=session1,froom=room1,exam_date=date1,fname=name1)
				#done.save()

			return render(request,'admin.html',{'data':data})
		#else:
		#		pass
		
		#for i in data:
			#print(i)

		#return render(request,'admin.html',{'data':data})
	#except Exception as e:
	#	print(e)
	#	return render(request,'admin.html',{'data':data})
	

def delete_all(request):
		
			delt()

			return redirect (admin_home)


def print_inv(request):

	pdf_conv(False,printinv(),"inv")
	return redirect (admin_home)
	

	pass
	
def print_all(request):
	
	
	#data=exam_inv.objects.values('exam_date','fname','froom').annotate(count=Count('exam_date')).filter(count__gt=0)
	#for dic in data:
	 #print(dic)
	#for date,Name,morning_ses,afternoon_ses  in data:
	#		print(date,Name,morning_ses,afternoon_ses)
	pdf_conv(True,print_al(),"all")
	
	print(print_al())
	
	return redirect (admin_home)
		
	pass
	
def print_dc(request):
	
	pdf_conv(False,printdc(),"dc")
	return redirect (admin_home)

	pass
	
def DUTY(request):


			names=fname_no_in_exam()
			val=[[],[]]
			for i in names:
				val[0].append(i[0])
				val[1].append(i[1])
		
			print(val[0],";;;;;;;;;;;;;;;;")
			
			dates=new()
			date_lst=[]
			
			for i in dates:
				date_lst.append(i[0])
			if  request.GET.get('done1'):
					print("seeeleted")
					date=[]
					date_1=[]
					id=request.GET.get("id")
					date.append(request.GET.get("name"))
					date.append(format_mon(request.GET.get("date")))
					print(date)
					date_1.append(format_mon(request.GET.get("date")))
					print(date_1)
					room1=room_1(exam_date=date[1])
					for room3 in room1:
						print(room3) 
					
					

					
					return render(request,'add_duty.html',{'room1':room1,'val':date,'date':date_1,'sep':'1','id':id})
			if  request.GET.get('done2'):
					print("seeeleted;;;;;;;;;;;;;;;;;;;;")
					date=[]
					date_1=[]
					id=request.GET.get("id")
					date.append(request.GET.get("name"))
					date.append(request.GET.get("date"))
					date.append(request.GET.get("room"))
					print(date)
					date_1.append(request.GET.get("date"))
					print(date_1)
					ses=ses_1(date[1],date[2])
					
					
					if len(ses)==2:
						ses='MA'
						print(True)
					print(val[0])
					if len(val[0]) ==0:
					
						return redirect(admin_home)
															
					else:
						
						return render(request,'add_duty.html',{'val':date,'sep':'1' ,'date':date_1, 'nov':'1','ses':ses,'id':id})
						
						pass

			
				#d#ate1=format_mon(request.GET.get("date"))
				#print(date,"///////////////////")
					#print(exam1)
					#return render(request,'edit.html',{'val':val,'id':id,'data':data,'faculty1':faculty1,'room1':room1,'exam1':exam1})
			if request.GET.get('done'):
				id=request.GET.get("id")
				print(id,";;;;;;;;;;;;;;;;;;;;;;;;")
				session1=request.GET.get("session")
				room1=request.GET.get("room")
				date1=str(request.GET.get("date"))
				print(date1)
				name1=request.GET.get("name")
				print(date1)
				done=exam_inv.objects.create(session=session1,froom=room1,exam_date=date1,fname=name1)
				#done.update(session=session1,froom=room1,exam_date=date1,fname=name1)
				done.save()

			
	
	
	
	#room1=room_1(exam_date=date[1])	
	#ses=ses_1(date[1],date([2])
			print(len(val))
			if val is not None:
				return redirect(admin_home)
				
			else:
				return render (request,'add_duty.html',{'val':val,'date':date_lst})
				pass
		
	
def admin_fac(request):

	
	try:	
		
		data=faculty.objects.all()

		if request.method=='GET':
			if request.GET.get('un') and request.GET.get('pw'):
				fname=request.GET.get('un')
				password=request.GET.get('pw')
				fac= faculty(fname=fname,password=password)
				fac.save()
				save_user(fname,password)
			
				#print(request.GET['un'],request.GET['pw'])
		
			if request.GET.get('inv') :
				
				id=request.GET.get('inv')
				
				inv=faculty.objects.get(id=id)
				if inv.inv_or_dc=='dc':
					ob=faculty.objects.filter(id=id).update(inv_or_dc="invigilator")
					
				else:
					ob=faculty.objects.filter(id=id).update(inv_or_dc="dc")
			if request.GET.get('Delete') :
				id=request.GET.get('Delete') 
				obj=faculty.objects.get(id=id)
				fname=faculty.objects.filter(id=id)
				for i in fname:
					fname=i.fname
					
				delete_user(fname)
				
				obj.delete()
				
				for i in fname:
					print(i.fname)
					print(i.id)
				

			if request.GET.get('edit') :
				
				id=request.GET.get('edit')
				obj=faculty.objects.filter(id=id)
				return render(request,'edit_fac_1.html',{'data':obj})
			if request.GET.get('done'):	
					password=request.GET.get('pass')
					id=request.GET.get('done')
					print(id,password,"''''''''''''''''''''''")
					obj=faculty.objects.filter(id=id).update(password=password)
				
					return redirect(admin_fac)
			
			if request.GET.get('Delete_all_fac'):
					 print("entered delete")
					 Delete_all_fac()
					 all_fac_is_staf()
					 return redirect(admin_fac)			
			
			return render(request,'admin_fac.html',{'data':data})
		
		
			pass
	except Exception as e:	
			
			print(e)
			data=faculty.objects.all()
			return render(request,'admin_fac.html',{'data':data})
	
	
def admin_room(request):

	if request.method=='GET':
		if request.GET.get('rm') :
			rm= room(roomno=request.GET.get('rm'))
			rm.save()
		data=room.objects.all()
		if request.GET.get('del') :
			pass		
		if request.GET.get('Delete') :
			
			id=request.GET.get('Delete') 
			obj=room.objects.get(roomno=id)
			obj.delete()
		if request.GET.get('del') :
			
				del_room()
		
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
				
		if request.GET.get('Delete'):
			
			id=request.GET.get('Delete')
			obj=exam.objects.get(id=id)
			obj.delete()
					
				
				
				
		if request.GET.get('del'):
				
				
				del_exam()		
			
			
			
		return render(request,'admin_exam.html',{'data':data,'exams':exams})
		pass
		


                 
def edit_fac(request):

	
	
	pass                 
            
                 
                
def logout(request):
                
                 get_out(request)
                 return  redirect (login)
                 

