from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Post

# Home page
def index(request):
    return render(request, 'main/index.html')

# About page
def about(request):
    return render(request, 'main/about.html')

# Signup page
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'main/signup.html')

# Login page
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'main/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('index')

# Community wall
def community(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST['message']
            Post.objects.create(user=request.user, text=text)
            return redirect('community')
        else:
            messages.error(request, "You must be logged in to post!")
            return redirect('login')

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main/community.html', {'posts': posts})


