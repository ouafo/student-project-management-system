from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from projekte.models import Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Registrierung erfolgreich! Bitte einloggen.')
            return redirect('login')
        # Fehler werden automatisch im Template angezeigt
    else:
        form = RegisterForm()
    return render(request, 'home/registrierung.html', {'form': form})

def startseite(request):
    return render(request, 'home/startseite.html')

def username_vergessen(request):
    gefundener_username = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            gefundener_username = user.username
        except User.DoesNotExist:
            messages.error(request, 'Kein Konto mit dieser E-Mail gefunden.')
    return render(request, 'home/username_vergessen.html', {
        'gefundener_username': gefundener_username
    })