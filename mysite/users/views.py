from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from users.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
# ----------------------------------------------------------------------------------------------


# sign up page
# ----------------------------------------------------------------------------------------------
def RegisterFunctionView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                'Welcome {}, you have been successfully signed up!'.format(username)
            )
            form.save()
            return redirect('food:home')

    else:
        form = RegisterForm(None)

    context = {
        "form": form
    }
   
    return render(request, "users/register.html", context)


# login page
# ----------------------------------------------------------------------------------------------
def LoginFunctionView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        auth_username = authenticate(request, username=username, password=password)
       
        if auth_username is None:
            messages.success(
                request,
                'Invalid Login, Try Again!'
            )
            return redirect('login')

        elif auth_username.is_superuser:
            login(request, auth_username)
            messages.success(
                request,
                'Superuser login accessed: {}'.format(auth_username)
            )
            return redirect('food:home')

        elif auth_username.is_authenticated:
            login(request, auth_username)
            messages.success(
                request,
                'Welcome {}, you have been successfully logged in!'.format(auth_username)
            )
            return redirect('food:home')

    return render(request, "users/login.html")


# logout page
# ----------------------------------------------------------------------------------------------

def LogoutFunctionView(request):
    username = request.user.username

    if request.method == 'POST':
        logout(request)
        messages.success(
            request,
            "{}, You have been successfully logged out!".format(username)
        )

        return redirect('login')

    context = {
        "username": username
    }
   
    return render(request, "users/logout.html", context)


# profile page
# ----------------------------------------------------------------------------------------------
@login_required
def ProfileFunctionView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "users/profile.html")