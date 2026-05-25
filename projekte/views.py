from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Mitgliedschaft, Profile
from .forms import ProjectForm, ProfilForm, PasswortForm
from django.contrib import messages


def get_user_info(user):
    # Wenn first_name gesetzt ist, direkt nehmen
    if user.first_name:
        vorname = user.first_name.capitalize()
        nachname = user.last_name.capitalize() if user.last_name else ""
    else:
        # Aus E-Mail ableiten
        email = user.email
        name_part = email.split("@")[0] if email else user.username
        parts = name_part.replace(".", " ").replace("-", " ").split()
        vorname = parts[0].capitalize() if len(parts) > 0 else user.username.capitalize()
        nachname = parts[1].capitalize() if len(parts) > 1 else ""

    fullname = f"{vorname} {nachname}".strip()
    avatar = f"{vorname[0]}{nachname[0] if nachname else ''}".upper()
    return vorname, nachname, fullname, avatar  # ← einheitliche Reihenfolge


@login_required
def dashboard_view(request):
    projekte = Project.objects.filter(mitgliedschaft_set__user=request.user).distinct()
    form = ProjectForm()
    form.fields['teilnehmer'].queryset = User.objects.exclude(id=request.user.id)
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
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.fields['teilnehmer'].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            projekt = form.save(commit=False)
            projekt.admin = request.user
            projekt.save()
            Mitgliedschaft.objects.get_or_create(user=request.user, project=projekt)
            teilnehmer = form.cleaned_data.get('teilnehmer')
            for user in teilnehmer:
                Mitgliedschaft.objects.get_or_create(user=user, project=projekt)

            messages.success(request, 'Projekt erfolgreich erstellt!!')
        else:
            messages.error(request, 'Projekt konnte niht erstellt werden')
    return redirect('dashboard')


@login_required
def projekt_loeschen(request, projekt_id):
    projekt = get_object_or_404(Project, id=projekt_id, admin=request.user)
    if request.method == 'POST':
        projekt.delete()
    return redirect('dashboard')

@login_required
def profil_bearbeiten(request):
    # Sicherstellen, dass ein Profil existiert
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        aktion = request.POST.get('aktion')

        if aktion == 'avatar_update':
            # Farbe ändern
            neue_farbe = request.POST.get('avatar_farbe')
            if neue_farbe:
                profile.avatar_farbe = neue_farbe
                messages.success(request, 'Farbe erfolgreich aktualisiert!')

            # Bild hochladen
            if 'avatar_datei' in request.FILES:
                profile.avatar_bild = request.FILES['avatar_datei']
                messages.success(request, 'Profilbild erfolgreich hochgeladen!')

            profile.save()
            return redirect('profil_bearbeiten')

        elif aktion == 'avatar_loeschen':
            # Fall 3: Bild entfernen
            if profile.avatar_bild:
                profile.avatar_bild.delete()  # Löscht die Datei vom Server
                profile.avatar_bild = None
                profile.save()
                messages.success(request, 'Profilbild entfernt. Farbe und Initialen sind nun aktiv.')
            return redirect('profil_bearbeiten')

    vorname, nachname, fullname, avatar = get_user_info(request.user)

    #Standardformulare vorab definieren (für GET-Requests und Fallbacks)
    profil_form = ProfilForm(initial={
        'vorname': request.user.first_name or vorname,
        'nachname': request.user.last_name or nachname,
        'email': request.user.email,
    })
    passwort_form = PasswortForm()

    if request.method == 'POST':
        aktion = request.POST.get('aktion')

        if aktion == 'profil':
            # Formular mit POST-Daten überschreiben
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
                    request.user.set_password(passwort_form.cleaned_data['neues_passwort'])
                    request.user.save()
                    messages.success(request, 'Passwort erfolgreich geändert!')
                    return redirect('profil_bearbeiten')
                else:
                    # Fehler für falsches aktuelles Passwort
                    messages.error(request, 'Das aktuelle Passwort ist falsch.')
            else:
                # Hier werden Validierungsfehler (z.B. "Passwörter stimmen nicht überein")
                for error in passwort_form.non_field_errors():
                    messages.error(request, error)

                for field in passwort_form: #passwort-fehler erscheinen als Toast oben auf der Seite
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")
        elif aktion == 'account_loeschen':
            request.user.delete()
            return redirect('dashboard')

    # Daten nach eventuellen Änderungen neu auslesen
    vorname, nachname, fullname, avatar = get_user_info(request.user)

    return render(request, 'profil_bearbeiten.html', {
        'profil_form': profil_form,
        'passwort_form': passwort_form,
        'fullname': fullname,
        'avatar': avatar,
        'vorname': vorname,
        'nachname': nachname,
    })

@login_required
def einstellungen(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    vorname, nachname, fullname, avatar = get_user_info(request.user)
    if request.method == 'POST':
        profile.notify_email = 'notify_email' in request.POST
        profile.notify_system = 'notify_system' in request.POST
        profile.kompakt_modus = 'kompakt_modus' in request.POST
        profile.sprache = request.POST.get('sprache', 'de')
        profile.profil_oeffentlich = ("profil_oeffentlich" in request.POST)
        profile.auffindbar = ("auffindbar" in request.POST)

        profile.save()
        messages.success(request, 'Einstellungen erfolgreich aktualisiert!')
        return redirect('dashboard')

    return render(request, 'einstellung.html', {
        'profile': profile,
        'avatar': avatar,
        'vorname': vorname
    })