from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from aufgaben.models import Aufgabe
from .models import Projekt, Mitgliedschaft, Profile, Notification
from .forms import ProjectForm, ProfilForm, PasswortForm
from django.contrib import messages
from .utils import send_notification
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
User = get_user_model()

def get_sidebar_context(user):
    """
    Gibt alle nötigen Daten für die Sidebar zurück
    → In allen Views benutzen!
    """
    from .models import Profile
    vorname, nachname, fullname, avatar = get_user_info(user)

    # Profil holen oder erstellen
    profile, created = Profile.objects.get_or_create(user=user)

    return {
        'vorname': vorname,
        'nachname': nachname,
        'fullname': fullname,
        'avatar': avatar,
        'profile': profile,
    }

def get_user_info(user):
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
    projekte = Projekt.objects.filter(
        mitgliedschaft_set__user=request.user
    ).distinct()

    form = ProjectForm()
    # FIX 1: Nur auffindbare User in der Teilnehmerliste anzeigen
    form.fields['teilnehmer'].queryset = User.objects.filter(
        profile__in_teilnehmerliste_auffindbar=True
    ).exclude(id=request.user.id)

    vorname, nachname, fullname, avatar = get_user_info(request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    # Aufgaben-Statistiken
    from aufgaben.models import Aufgabe
    aufgaben_erledigt = Aufgabe.objects.filter(
        projekt__mitgliedschaft_set__user=request.user,
        status=Aufgabe.Status.ERLEDIGT
    ).distinct().count()
    aufgaben_offen = Aufgabe.objects.filter(
        projekt__mitgliedschaft_set__user=request.user
    ).exclude(status=Aufgabe.Status.ERLEDIGT).distinct().count()

    return render(request, 'Projekt_view.html', {
        'projekte': projekte,
        'form': form,
        'fullname': fullname,
        'avatar': avatar,
        'vorname': vorname,
        'aufgaben_erledigt': aufgaben_erledigt,
        'aufgaben_offen': aufgaben_offen,
    })


@login_required
def projekt_erstellen(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.fields['teilnehmer'].queryset = User.objects.filter(
            profile__in_teilnehmerliste_auffindbar=True
        ).exclude(id=request.user.id)
        if form.is_valid():
            projekt = form.save(commit=False)
            projekt.admin = request.user
            projekt.save()
            Mitgliedschaft.objects.get_or_create(user=request.user, projekt=projekt)
            teilnehmer = form.cleaned_data.get('teilnehmer')
            for user in teilnehmer:
                Mitgliedschaft.objects.get_or_create(user=user, projekt=projekt)
                send_notification(
                    user=user,
                    title="Du wurdest einem Projekt hinzugefügt!",
                    message=f"{request.user.username} hat dich zum Projekt '{projekt.titel}' hinzugefügt.",
                    notification_type="projekt"
                )
            messages.success(request, 'Projekt erfolgreich erstellt!')
        else:
            messages.error(request, 'Projekt konnte nicht erstellt werden.')
    return redirect('dashboard')


@login_required
def projekt_loeschen(request, projekt_id):
    projekt = get_object_or_404(Projekt, id=projekt_id, admin=request.user)
    if request.method == 'POST':
        projekt.delete()
    return redirect('dashboard')


@login_required
def profil_bearbeiten(request):
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
                messages.success(request, 'Profilbild entfernt.')
            return redirect('profil_bearbeiten')

    vorname, nachname, fullname, avatar = get_user_info(request.user)
    profil_form = ProfilForm(initial={
        'vorname': request.user.first_name or vorname,
        'nachname': request.user.last_name or nachname,
        'email': request.user.email,
    })
    passwort_form = PasswortForm()

    if request.method == 'POST':
        aktion = request.POST.get('aktion')
        if aktion == 'profil':
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
                    messages.error(request, 'Das aktuelle Passwort ist falsch.')
            else:
                for error in passwort_form.non_field_errors():
                    messages.error(request, error)
                for field in passwort_form:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")

        elif aktion == 'account_loeschen':
            request.user.delete()
            return redirect('dashboard')

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
        profile.profil_oeffentlich = 'profil_oeffentlich' in request.POST
        # FIX 2: richtiger Feldname
        profile.in_teilnehmerliste_auffindbar = 'auffindbar' in request.POST
        profile.notify_projekt = 'notify_projekt' in request.POST
        profile.notify_deadline = 'notify_deadline' in request.POST
        profile.save()
        messages.success(request, 'Einstellungen erfolgreich aktualisiert!')
        return redirect('dashboard')

    return render(request, 'einstellung.html', {
        'profile': profile,
        'avatar': avatar,
        'vorname': vorname,
    })


@login_required
def konto_loeschen_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Konto erfolgreich gelöscht.")
        return redirect('startseite')
    return redirect('startseite')


def benachrichtigung_lesen(request, pk):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
def globale_suche(request):
    query = request.GET.get('q', '')
    projekt_ergebnisse = []
    profil_ergebnisse = []

    if query:
        # FIX 3: Sichtbarkeitsregeln korrekt anwenden
        projekt_ergebnisse = Projekt.objects.filter(
            Q(titel__icontains=query) | Q(beschreibung__icontains=query)
        ).filter(
            Q(admin=request.user) |
            Q(mitgliedschaft_set__user=request.user) |
            Q(projekte_oeffentlich=True, nur_mitgliederzugriff=False)
        ).distinct()

        profil_ergebnisse = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            profile__profil_oeffentlich=True
        ).exclude(id=request.user.id)

    return render(request, 'projekte/suche_ergebnisse.html', {
        'query': query,
        'projekt_ergebnisse': projekt_ergebnisse,
        'profil_ergebnisse': profil_ergebnisse,
    })


@login_required
def projekt_detail(request, projekt_id):
    projekt = get_object_or_404(Projekt, id=projekt_id)
    ist_mitglied = projekt.mitgliedschaft_set.filter(user=request.user).exists()
    ist_admin = (projekt.admin == request.user)
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
    if projekt.nur_mitgliederzugriff and not (ist_mitglied or ist_admin):
        return HttpResponseForbidden("Zugriff verweigert: Dieses Projekt ist privat.")
    return render(request, 'projekte/detail.html', {
        'projekt': projekt,
        'aufgaben': alle_aufgaben,
        'gesamt': gesamt,
        'offen': anzahl_offen,
        'in_bearbeitung': anzahl_in_bearbeitung,
        'in_ueberpruefung': anzahl_in_ueberpruefung,
        'erledigt': anzahl_erledigt,
    })