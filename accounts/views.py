from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrierungsForm, LoginForm

# Create your views here.

def registrierung(request):
    """Benutzerregistrierung"""
    # Falls bereits eingeloggt → Dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrierungsForm(request.POST)
        if form.is_valid():
            benutzer = form.save()
            login(request, benutzer)
            messages.success(
                request,
                f'Willkommen bei Boardify, {benutzer.username}! 🎉'
            )
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Bitte korrigiere die Fehler!'
            )
    else:
        form = RegistrierungsForm()

    return render(request, 'accounts/registrierung.html', {
        'form': form
    })


def benutzer_login(request):
    """Benutzer Login"""
    # Falls bereits eingeloggt → Dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            benutzer = authenticate(
                request,
                username=username,
                password=password
            )
            if benutzer is not None:
                login(request, benutzer)
                messages.success(
                    request,
                    f'Willkommen zurück, {benutzer.username}! 👋'
                )
                return redirect('dashboard')
        else:
            messages.error(
                request,
                'Benutzername oder Passwort falsch!'
            )
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def benutzer_logout(request):
    """Benutzer Logout"""
    logout(request)
    messages.info(
        request,
        'Du wurdest erfolgreich abgemeldet!'
    )
    return redirect('login')


@login_required
def dashboard(request):
    """Dashboard — nur für eingeloggte Benutzer"""
    return render(request, 'dashboard.html', {
        'benutzer': request.user
    })
