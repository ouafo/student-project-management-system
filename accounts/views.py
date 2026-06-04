from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import RegisterForm

User = get_user_model()


def startseite(request):
    """Startseite"""
    return render(request, 'accounts/startseite.html')


def register(request):
    """Benutzerregistrierung"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['passwort'])
            user.save()

            messages.success(
                request,
                'Registrierung erfolgreich! Bitte einloggen.'
            )
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/registrierung.html', {
        'form': form
    })


def benutzer_login(request):
    """Benutzer Login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            messages.success(
                request,
                f'Willkommen zurück, {user.username}! 👋'
            )
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Benutzername oder Passwort falsch!'
            )
    return render(request, 'accounts/login.html')


def benutzer_logout(request):
    """Benutzer Logout"""
    logout(request)
    messages.info(
        request,
        'Du wurdest erfolgreich abgemeldet!'
    )
    return redirect('startseite')


def username_vergessen(request):
    """Username vergessen"""
    gefundener_username = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            gefundener_username = user.username
        except User.DoesNotExist:
            messages.error(
                request,
                'Kein Konto mit dieser E-Mail gefunden.'
            )
    return render(request, 'accounts/username_vergessen.html', {
        'gefundener_username': gefundener_username
    })