from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from accounts.models import Benutzer
from .models import Projekt, Mitgliedschaft, Profile
from .forms import ProjectForm, ProfilForm, PasswortForm
from aufgaben.models import Aufgabe


def get_user_info(user):
    """Benutzer Informationen ermitteln"""
    if user.first_name:
        vorname = user.first_name.capitalize()
        nachname = user.last_name.capitalize() if user.last_name else ""
    else:
        email = user.email
        name_part = email.split("@")[0] if email else user.username
        parts = name_part.replace(".", " ").replace("-", " ").split()
        vorname = parts[0].capitalize() if len(parts) > 0 else user.username.capitalize()
        nachname = parts[1].capitalize() if len(parts) > 1 else ""

    fullname = f"{vorname} {nachname}".strip()
    avatar = f"{vorname[0]}{nachname[0] if nachname else ''}".upper()
    return vorname, nachname, fullname, avatar


@login_required
def dashboard_view(request):
    """Dashboard — Alle Projekte des Benutzers"""
    projekte = Projekt.objects.filter(
        mitgliedschaft_set__user=request.user
    ).distinct()
    form = ProjectForm()
    form.fields['teilnehmer'].queryset = Benutzer.objects.exclude(
        id=request.user.id
    )
    vorname, nachname, fullname, avatar = get_user_info(request.user)
    return render(request, 'Projekt_view.html', {
        'projekte': projekte,
        'form': form,
        'fullname': fullname,
        'avatar': avatar,
        'vorname': vorname,
    })


@login_required
def projekt_erstellen(request):
    """Neues Projekt erstellen"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.fields['teilnehmer'].queryset = Benutzer.objects.exclude(
            id=request.user.id
        )
        if form.is_valid():
            projekt = form.save(commit=False)
            projekt.admin = request.user
            projekt.save()
            Mitgliedschaft.objects.get_or_create(
                user=request.user,
                projekt=projekt
            )
            teilnehmer = form.cleaned_data.get('teilnehmer')
            for user in teilnehmer:
                Mitgliedschaft.objects.get_or_create(
                    user=user,
                    projekt=projekt
                )
            messages.success(request, 'Projekt erfolgreich erstellt!')
        else:
            messages.error(request, 'Projekt konnte nicht erstellt werden!')
    return redirect('dashboard')


@login_required
def projekt_loeschen(request, projekt_id):
    """Projekt löschen"""
    projekt = get_object_or_404(
        Projekt,
        id=projekt_id,
        admin=request.user
    )
    if request.method == 'POST':
        projekt.delete()
        messages.success(request, 'Projekt erfolgreich gelöscht!')
    return redirect('dashboard')


@login_required
def projekt_detail(request, projekt_id):
    """Projekt Detail mit Aufgabenliste"""
    projekt = get_object_or_404(Projekt, id=projekt_id)

    alle_aufgaben = Aufgabe.objects.filter(
        projekt=projekt
    ).order_by('status', '-erstellt_am')

    gesamt = alle_aufgaben.count()
    anzahl_offen = alle_aufgaben.filter(status='offen').count()
    anzahl_in_bearbeitung = alle_aufgaben.filter(
        status='in_bearbeitung'
    ).count()
    anzahl_in_ueberpruefung = alle_aufgaben.filter(
        status='in_ueberpruefung'
    ).count()
    anzahl_erledigt = alle_aufgaben.filter(status='erledigt').count()

    return render(request, 'projekte/detail.html', {
        'projekt': projekt,
        'aufgaben': alle_aufgaben,
        'gesamt': gesamt,
        'offen': anzahl_offen,
        'in_bearbeitung': anzahl_in_bearbeitung,
        'in_ueberpruefung': anzahl_in_ueberpruefung,
        'erledigt': anzahl_erledigt,
    })


@login_required
def profil_bearbeiten(request):
    """Profil bearbeiten"""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        aktion = request.POST.get('aktion')

        if aktion == 'avatar_update':
            neue_farbe = request.POST.get('avatar_farbe')
            if neue_farbe:
                profile.avatar_farbe = neue_farbe
                messages.success(request, 'Farbe erfolgreich aktualisiert!')
            if 'avatar_datei' in request.FILES:
                profile.avatar_bild = request.FILES['avatar_datei']
                messages.success(request, 'Profilbild erfolgreich hochgeladen!')
            profile.save()
            return redirect('profil_bearbeiten')

        elif aktion == 'avatar_loeschen':
            if profile.avatar_bild:
                profile.avatar_bild.delete()
                profile.avatar_bild = None
                profile.save()
                messages.success(request, 'Profilbild entfernt!')
            return redirect('profil_bearbeiten')

        elif aktion == 'profil':
            profil_form = ProfilForm(request.POST)
            if profil_form.is_valid():
                request.user.first_name = profil_form.cleaned_data['vorname']
                request.user.last_name = profil_form.cleaned_data['nachname']
                request.user.email = profil_form.cleaned_data['email']
                request.user.save()
                messages.success(request, 'Profil erfolgreich aktualisiert!')
                return redirect('profil_bearbeiten')

        elif aktion == 'passwort':
            passwort_form = PasswortForm(request.POST)
            if passwort_form.is_valid():
                altes_pw = passwort_form.cleaned_data['altes_passwort']
                if request.user.check_password(altes_pw):
                    request.user.set_password(
                        passwort_form.cleaned_data['neues_passwort']
                    )
                    request.user.save()
                    messages.success(request, 'Passwort erfolgreich geändert!')
                    return redirect('profil_bearbeiten')
                else:
                    messages.error(request, 'Das aktuelle Passwort ist falsch!')

        elif aktion == 'account_loeschen':
            request.user.delete()
            return redirect('dashboard')

    vorname, nachname, fullname, avatar = get_user_info(request.user)
    profil_form = ProfilForm(initial={
        'vorname': request.user.first_name or vorname,
        'nachname': request.user.last_name or nachname,
        'email': request.user.email,
    })
    passwort_form = PasswortForm()

    return render(request, 'profil_bearbeiten.html', {
        'profil_form': profil_form,
        'passwort_form': passwort_form,
        'fullname': fullname,
        'avatar': avatar,
        'vorname': vorname,
        'nachname': nachname,
        'profile': profile,
    })


@login_required
def einstellungen(request):
    """Einstellungen"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    vorname, nachname, fullname, avatar = get_user_info(request.user)

    if request.method == 'POST':
        profile.notify_email = 'notify_email' in request.POST
        profile.notify_system = 'notify_system' in request.POST
        profile.kompakt_modus = 'kompakt_modus' in request.POST
        profile.sprache = request.POST.get('sprache', 'de')
        profile.save()
        messages.success(request, 'Einstellungen erfolgreich aktualisiert!')
        return redirect('dashboard')

    return render(request, 'einstellung.html', {
        'profile': profile,
        'avatar': avatar,
        'vorname': vorname
    })