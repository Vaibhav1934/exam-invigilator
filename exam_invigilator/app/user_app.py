from django.contrib.auth import authenticate
from django.contrib.auth.models import User,auth

def save_user(username,password):
	
	user,created=User.objects.get_or_create(username= username)

	try:	
		if created:	
			user.set_password(password)
			user.save()
	
		else:
	
			user=User.objects.create_user(username= username,password=password)
	except Exception as e :
		
		print(e, ' didt work ')
	
def auth(username,password):
	user=authenticate(username= username, password=password)
	print('.....................' ,user)
	return user
