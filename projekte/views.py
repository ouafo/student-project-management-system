from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Projekt
from aufgaben.models import Aufgabe
import json
# Create your views here.


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
    alle_aufgaben = Aufgabe.objects.filter(projekt=projekt).order_by('status', '-erstellt_am')

    # Statistiken
    gesamt = alle_aufgaben.count()
    offen = alle_aufgaben.filter(status='offen').count()
    in_bearbeitung = alle_aufgaben.filter(status='in_bearbeitung').count()
    in_ueberpruefung = alle_aufgaben.filter(status='in_ueberpruefung').count()
    erledigt = alle_aufgaben.filter(status='erledigt').count()

    return render(request, 'projekte/detail.html', {
        'projekt': projekt,
        'aufgaben': alle_aufgaben,
        'gesamt': gesamt,
        'offen': offen,
        'in_bearbeitung': in_bearbeitung,
        'in_ueberpruefung': in_ueberpruefung,
        'erledigt': erledigt,
    })


@login_required
def kanban_board(request, projekt_id):
    """Kanban Board eines Projekts"""
    projekt = get_object_or_404(Projekt, id=projekt_id)

    # Aufgaben nach Status gruppieren
    offen = Aufgabe.objects.filter(
        projekt=projekt,
        status='offen'
    )
    in_bearbeitung = Aufgabe.objects.filter(
        projekt=projekt,
        status='in_bearbeitung'
    )
    in_ueberpruefung = Aufgabe.objects.filter(
        projekt=projekt,
        status='in_ueberpruefung'
    )
    erledigt = Aufgabe.objects.filter(
        projekt=projekt,
        status='erledigt'
    )

    return render(request, 'projekte/kanban.html', {
        'projekt': projekt,
        'offen': offen,
        'in_bearbeitung': in_bearbeitung,
        'in_ueberpruefung': in_ueberpruefung,
        'erledigt': erledigt,
    })

@csrf_exempt
@login_required
@require_POST
def aufgabe_status_update(request, aufgabe_id):

    try:
        daten = json.loads(request.body)
        neuer_status = daten.get('status')

        gueltige_status = [
            'offen',
            'in_bearbeitung',
            'in_ueberpruefung',
            'erledigt'
        ]

        if neuer_status not in gueltige_status:
            return JsonResponse({
                'success': False,
                'error': 'ungültiger Status!'
            }, status=400)

        aufgabe = get_object_or_404(Aufgabe, id=aufgabe_id)
        aufgabe.status = neuer_status
        aufgabe.save()

        return JsonResponse({
            'success': True,
            'message': f'Status auf {neuer_status} geändert!',
            'aufgabe_id': aufgabe_id,
            'neuer_status': neuer_status
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Ungültige Daten!'
        },status=400)