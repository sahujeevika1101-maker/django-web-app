from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Item  # jis model par CRUD ho raha hai

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if username and password == confirm:
            User.objects.create_user(username=username, password=password)
            return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    items = Item.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"items": items})

from django.shortcuts import render, redirect
from .models import Item

def create_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        title = request.POST.get("title")
        if title:  # empty title avoid karne ke liye
            Item.objects.create(user=request.user, title=title)
            return redirect("dashboard")

    return render(request, "create.html")
    return render(request, "create.html")

def update_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")

    item = get_object_or_404(Item, id=pk, user=request.user)

    if request.method == "POST":
        item.title = request.POST.get("title")
        item.save()
        return redirect("dashboard")

    return render(request, "update.html", {"item": item})

def delete_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")

    item = get_object_or_404(Item, id=pk, user=request.user)
    item.delete()
    return redirect("dashboard")