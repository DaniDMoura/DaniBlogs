import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from .models import *

def post_list(request):
    posts = Post.objects.all()

    if request.method == "POST":
        title = request.POST.get("search", "").strip()
        if title:
            posts = posts.filter(title__icontains=title)

    for post in posts:
        post.truncated_content = post.content[:100] + "..." if len(post.content) > 150 else post.content

    return render(request, "post_list.html", {"posts": posts})

@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "post_details.html", {"post": post})

@login_required
def add_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not all([title, content]):
            messages.error(request, "Title and content cannot be empty.")
            return redirect("add_page")

        Post.objects.create(title=title, content=content)
        messages.success(request, "Post created successfully!")
        return redirect("/")

    return render(request, "add.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error_message": "Invalid username or password."})

    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print(f"First Name: {first_name}, Last Name: {last_name}, Username: {username}, Email: {email}")

        if not all([first_name, last_name, email, username, password, confirm_password]):
            return render(request, "signup.html", {"log": "Fields cannot be left blank"})

        if password != confirm_password:
            return render(request, "signup.html", {"log": "Passwords do not match"})

        if Signup.objects.filter(username=username).exists():
            return render(request, "signup.html", {"log": "Username is already taken"})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render(request, "signup.html", {"log": "Invalid email format"})

        if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            return render(
                request, "signup.html",
                {"log": "Password must be at least 8 characters long and contain both letters and numbers"}
            )

        if " " in username:
            return render(request, "signup.html", {"log": "Username cannot contain spaces"})

        User = get_user_model()
        user = Signup.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()



        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "signup.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')