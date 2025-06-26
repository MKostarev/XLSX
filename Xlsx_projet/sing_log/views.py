from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('thanks')  # Используем имя URL, не путь
    else:
        form = UserCreationForm()
    return render(request, 'sing_log/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Используем имя URL
    else:
        form = AuthenticationForm()
    return render(request, 'sing_log/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Используем имя URL, не путь к шаблону

def home_view(request):
    if request.user.is_authenticated:
        return redirect('upload_files:upload_file')
    return render(request, 'sing_log/home.html')

def thanks_view(request):
    return render(request, 'sing_log/thanks.html')

