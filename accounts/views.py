from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from projekte.models import Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Registrierung erfolgreich! Bitte einloggen.')
            return redirect('login')
        # Fehler werden automatisch im Template angezeigt
    else:
        form = RegisterForm()
    return render(request, 'home/registrierung.html', {'form': form})

def startseite(request):
    return render(request, 'home/startseite.html')
