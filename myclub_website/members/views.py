from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if user.is_superuser:
				#messages.success(request, ("You have logged in"))
				return redirect('admin_approval')
			else:
				#messages.success(request, ("You have logged in"))
				return redirect('home')
		else:
			#return an 'invalid login' error message
			messages.success(request, ("Invalid login credentials. Please try again."))
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})



def logout_user(request):
	logout(request)
	messages.success(request, ("You were logged out"))
	return redirect('home')


def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('Registration Successfull'))
			return redirect('login')
	else:
		form = RegisterUserForm()

	return render(request, 'authenticate/register_user.html', {'form':form})