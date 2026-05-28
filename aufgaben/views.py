from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import AufgabeForm, KommentarForm, StatusForm, ChatNachrichtForm
from .models import Aufgabe, ChatNachricht, Kommentar


@login_required
def aufgabe_detail(request, pk):
    """Aufgabe Detail mit Kommentaren"""
    aufgabe = get_object_or_404(
        Aufgabe.objects.select_related(
            "zugewiesen_an",
            "erstellt_von",
            "projekt"
        ).prefetch_related("kommentare__autor"),
        pk=pk
    )

    kommentar_form = KommentarForm()
    status_form = StatusForm(instance=aufgabe)

    if request.method == "POST":
        if "kommentar_absenden" in request.POST:
            kommentar_form = KommentarForm(request.POST)
            if kommentar_form.is_valid():
                kommentar = kommentar_form.save(commit=False)
                kommentar.aufgabe = aufgabe
                kommentar.autor = request.user
                kommentar.save()
                messages.success(request, "Kommentar wurde hinzugefügt.")
                return redirect("aufgabe_detail", pk=aufgabe.pk)

        elif "status_speichern" in request.POST:
            status_form = StatusForm(request.POST, instance=aufgabe)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Status wurde aktualisiert.")
                return redirect("aufgabe_detail", pk=aufgabe.pk)

    context = {
        "aufgabe": aufgabe,
        "kommentare": aufgabe.kommentare.select_related("autor").all(),
        "kommentar_form": kommentar_form,
        "status_form": status_form,
    }
    return render(request, "aufgaben/aufgabe_detail.html", context)


@login_required
def aufgabe_erstellen(request, projekt_id=None):
    """Neue Aufgabe erstellen"""
    from projekte.models import Projekt

    # Projekt holen falls vorhanden
    projekt = None
    if projekt_id:
        projekt = get_object_or_404(Projekt, id=projekt_id)

    if request.method == "POST":
        form = AufgabeForm(request.POST)
        if form.is_valid():
            aufgabe = form.save(commit=False)
            aufgabe.erstellt_von = request.user
            if projekt and not aufgabe.projekt_id:
                aufgabe.projekt = projekt
            aufgabe.save()
            messages.success(request, "Aufgabe wurde erstellt.")
            if aufgabe.projekt:
                return redirect(
                    "kanban_board",
                    projekt_id=aufgabe.projekt.id
                )
            return redirect("aufgabe_detail", pk=aufgabe.pk)
    else:
        initial = {}
        if projekt_id:
            initial['projekt'] = projekt_id
        form = AufgabeForm(initial=initial)

    return render(request, "aufgaben/aufgabe_form.html", {
        "form": form,
        "seite_titel": "Neue Aufgabe",
        "projekt_id": projekt_id,
        "projekt": projekt,  #  Projekt Objekt übergeben!
    })


@login_required
def aufgabe_bearbeiten(request, pk):
    """Aufgabe bearbeiten"""
    aufgabe = get_object_or_404(Aufgabe, pk=pk)
    projekt = aufgabe.projekt  #  Projekt holen!

    if request.method == "POST":
        form = AufgabeForm(request.POST, instance=aufgabe)
        if form.is_valid():
            form.save()
            messages.success(request, "Aufgabe wurde bearbeitet.")
            #  Zurück zur Detail Seite
            return redirect("aufgabe_detail", pk=aufgabe.pk)
    else:
        form = AufgabeForm(instance=aufgabe)

    return render(request, "aufgaben/aufgabe_form.html", {
        "form": form,
        "seite_titel": "Aufgabe bearbeiten",
        "projekt": projekt,      #  Projekt übergeben!
        "aufgabe": aufgabe,      #  Aufgabe übergeben!
    })


@login_required
def aufgabe_loeschen(request, pk):
    """Aufgabe löschen"""
    aufgabe = get_object_or_404(Aufgabe, pk=pk)
    projekt_id = aufgabe.projekt.id if aufgabe.projekt else None

    if request.method == "POST":
        aufgabe.delete()
        messages.success(request, "Aufgabe wurde gelöscht.")
        if projekt_id:
            return redirect("kanban_board", projekt_id=projekt_id)
        return redirect("dashboard")

    return render(request, "aufgaben/aufgabe_confirm_delete.html", {
        "aufgabe": aufgabe
    })


@login_required
def chat_view(request):
    """Chat Nachrichten"""
    nachrichten = ChatNachricht.objects.filter(
        Q(sender=request.user) | Q(empfaenger=request.user)
    ).select_related("sender", "empfaenger")

    if request.method == "POST":
        form = ChatNachrichtForm(request.POST, aktueller_user=request.user)
        if form.is_valid():
            nachricht = form.save(commit=False)
            nachricht.sender = request.user
            nachricht.save()
            messages.success(request, "Nachricht wurde gesendet.")
            return redirect("chat")
    else:
        form = ChatNachrichtForm(aktueller_user=request.user)

    return render(request, "aufgaben/chat.html", {
        "nachrichten": nachrichten,
        "form": form,
    })