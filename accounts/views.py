from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.

def register(request):
	if request.method == 'POST':
		#get form values
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']

		#validation
		if password == password2:
			if User.objects.filter(username=username).exists():
				messages.error(request,'Username already exists')
				return redirect('register')
			else:
				if User.objects.filter(email=email).exists():
					messages.error(request,'email already exists')
					return redirect('register')
				else:
					#looks good
					user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
					#login after reg
					#auth.login(request,user)
					#messages.success(request,'register successfully ,now logged in')
					#redirect('index')
					user.save()
					messages.success(request,'register successfully')
					return redirect('login')
		else:
			messages.error(request,'Passwords do not match')
			return redirect('register')
	else:
		return render(request, 'accounts/register.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			messages.success(request,'logged In successfully')
			return redirect('dashboard')
		else:
			messages.error(request,'user not found')
			return redirect('login')
	else:
		return render(request, 'accounts/login.html')

def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		messages.success(request,'you have successfully logout')
		return redirect('index')

def dashboard(request):
	return render(request, 'accounts/dashboard.html')
