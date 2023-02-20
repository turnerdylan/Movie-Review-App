from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def signupaccount(request):
    #check if get or post request, post is for creation, get is for retrieval
    if request.method == 'GET':
        #user is navigating to page from signupaccount url, so render page
        return render(request, 'signupaccount.html', {'form':UserCreateForm})
    else:
        #they are on the page already and submitting the form
        if request.POST['password1'] == request.POST['password2']:
            try:
                #create user obj w user and pw
                user = User.objects.create_user(
                    request.POST['username'], 
                    password = request.POST['password1'])
                #save user to db
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(
                    request, 
                    'signupaccount.html',
                    {
                        'form':UserCreateForm,
                        'error':'Username already exists'
                    })
        else:
            return render(request, 'signupaccount.html',
            {
                'form':UserCreateForm,
                'error':'Passwords dont match!'
            })

@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')

def loginaccount(request):
    if request.method == 'GET':
        #login page is being pulled up
        return render(request, 'loginaccount.html', {'form':AuthenticationForm})
    else:
        #form is being submitted
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'loginaccount.html',
            {
                'form': AuthenticationForm(),
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')