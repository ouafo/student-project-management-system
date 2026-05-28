from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from projekte.models import Projekt
from aufgaben.models import Aufgabe
import json
from projekte.views import get_sidebar_context

# Create your views here.
@login_required
def kanban_board(request, projekt_id):
    projekt = get_object_or_404(Projekt, id=projekt_id)

    offen = Aufgabe.objects.filter(
        projekt=projekt, status='offen'
    )
    in_bearbeitung = Aufgabe.objects.filter(
        projekt=projekt, status='in_bearbeitung'
    )
    in_ueberpruefung = Aufgabe.objects.filter(
        projekt=projekt, status='in_ueberpruefung'
    )
    erledigt = Aufgabe.objects.filter(
        projekt=projekt, status='erledigt'
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

    return render(request, 'kanban/kanban.html', {
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
    """Drag & Drop → Status aktualisieren"""
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
                'error': 'Ungültiger Status!'
            }, status=400)

        aufgabe = get_object_or_404(Aufgabe, id=aufgabe_id)
        alter_status = aufgabe.status
        aufgabe.status = neuer_status
        aufgabe.save()

        aufgabe.refresh_from_db()
        print(f"✅ Aufgabe {aufgabe_id}: {alter_status} → {aufgabe.status}")

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
        print(f"❌ Fehler: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)