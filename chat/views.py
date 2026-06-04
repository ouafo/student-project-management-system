
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from projekte.models import Projekt, Mitgliedschaft
from .models import ChatNachricht

logger = logging.getLogger(__name__)

@login_required
def chat_view(request, projekt_id):
    projekt = get_object_or_404(Projekt, id=projekt_id)

    # ── Zugriffsprüfung: nur Projektmitglieder ─────────────────
    ist_mitglied = Mitgliedschaft.objects.filter(
        projekt=projekt,
        user=request.user
    ).exists()

    if not ist_mitglied:
        logger.warning(
            "Benutzer %s hat versucht, auf Chat von Projekt %s zuzugreifen.",
            request.user.username, projekt_id
        )
        return redirect('dashboard')

    # ── POST: Nachricht speichern ───────────────────────────────
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            ChatNachricht.objects.create(
                projekt=projekt,
                sender=request.user,
                text=text
            )
        return redirect('chat', projekt_id=projekt_id)

    # ── GET: Nachrichten + Mitglieder laden ─────────────────────
    nachrichten = ChatNachricht.objects.filter(
                    projekt=projekt
                  ).select_related('sender')

    Benutzer = get_user_model()
    mitglieder = Benutzer.objects.filter(
                    mitgliedschaften__projekt=projekt
                 ).distinct()

    return render(request, 'aufgaben/chat.html', {
        'projekt'    : projekt,
        'nachrichten': nachrichten,
        'mitglieder' : mitglieder,
    })