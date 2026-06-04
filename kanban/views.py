from random import choice

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from projekte.models import Projekt
from aufgaben.models import Aufgabe
import json
from projekte.views import get_sidebar_context

import logging
logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def kanban_board(request, projekt_id):
    projekt = get_object_or_404(Projekt, id=projekt_id)

    offen = Aufgabe.objects.filter(
        projekt=projekt, status=Aufgabe.Status.OFFEN
    )
    in_bearbeitung = Aufgabe.objects.filter(
        projekt=projekt, status=Aufgabe.Status.IN_BEARBEITUNG
    )
    in_ueberpruefung = Aufgabe.objects.filter(
        projekt=projekt, status=Aufgabe.Status.IN_UEBERPRUEFUNG
    )
    erledigt = Aufgabe.objects.filter(
        projekt=projekt, status=Aufgabe.Status.ERLEDIGT
    )

    #  Sidebar Context hinzufügen!
    context = get_sidebar_context(request.user)
    context.update({
        'projekt': projekt,
        'offen': offen,
        'in_bearbeitung': in_bearbeitung,
        'in_ueberpruefung': in_ueberpruefung,
        'erledigt': erledigt,
    })
    return render(request, 'kanban/kanban.html', context)



@login_required
@require_POST
def aufgabe_status_update(request, aufgabe_id):
    """Drag & Drop → Status aktualisieren"""
    try:
        daten = json.loads(request.body)
        neuer_status = daten.get('status')

        gueltige_status = [choice.value for choice in Aufgabe.Status]

        if neuer_status not in gueltige_status:
            return JsonResponse({
                'success': False,
                'error': 'Ungültiger Status!'
            }, status=400)

        aufgabe = get_object_or_404(Aufgabe, id=aufgabe_id)
        ist_mitglied = aufgabe.projekt.mitgliedschaft_set.filter(user=request.user).exists()
        ist_admin = (aufgabe.projekt.admin == request.user)
        if not (ist_mitglied or ist_admin):
            return JsonResponse({'success': False, 'error': 'Keine Berechtigung!'}, status=403)
        alter_status = aufgabe.status
        aufgabe.status = neuer_status
        aufgabe.save()

        aufgabe.refresh_from_db()
        logger.info(f"Aufgabe {aufgabe_id}: {alter_status} → {aufgabe.status}")

        return JsonResponse({
            'success': True,
            'message': f'Status geändert!',
            'aufgabe_id': aufgabe_id,
            'neuer_status': aufgabe.status
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Ungültige Daten!'
        }, status=400)
    except Exception as e:
        logger.error(f"Fehler bei Status-Update: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)