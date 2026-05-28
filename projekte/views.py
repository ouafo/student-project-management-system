from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from aufgaben.models import Aufgabe
from .models import Projekt


@login_required
def projekt_liste(request):
    """Alle Projekte des Benutzers"""
    projekte = Projekt.objects.filter(
        besitzer=request.user
    )
    return render(request, 'projekte/liste.html', {
        'projekte': projekte
    })


@login_required
def projekt_detail(request, projekt_id):
    """Projekt Detail mit Aufgabenliste"""
    projekt = get_object_or_404(Projekt, id=projekt_id)

    alle_aufgaben = Aufgabe.objects.filter(
        projekt=projekt
    ).order_by('status', '-erstellt_am')

    gesamt = alle_aufgaben.count()
    anzahl_offen = alle_aufgaben.filter(
        status='offen'
    ).count()
    anzahl_in_bearbeitung = alle_aufgaben.filter(
        status='in_bearbeitung'
    ).count()
    anzahl_in_ueberpruefung = alle_aufgaben.filter(
        status='in_ueberpruefung'
    ).count()
    anzahl_erledigt = alle_aufgaben.filter(
        status='erledigt'
    ).count()

    return render(request, 'projekte/detail.html', {
        'projekt': projekt,
        'aufgaben': alle_aufgaben,
        'gesamt': gesamt,
        'offen': anzahl_offen,
        'in_bearbeitung': anzahl_in_bearbeitung,
        'in_ueberpruefung': anzahl_in_ueberpruefung,
        'erledigt': anzahl_erledigt,
    })