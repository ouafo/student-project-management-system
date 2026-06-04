import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from kommentare.forms import KommentarForm
from projekte.models import Projekt
from .forms import AufgabeForm, StatusForm
from .models import Aufgabe

logger = logging.getLogger(__name__)


@login_required
def aufgabe_detail(request, pk):
    aufgabe = get_object_or_404(
        Aufgabe.objects.select_related(
            "zugewiesen_an", "erstellt_von", "projekt"
        ).prefetch_related("kommentare__autor"),
        pk=pk
    )

    kommentar_form = KommentarForm()
    status_form    = StatusForm(instance=aufgabe)

    if request.method == "POST":
        if "kommentar_absenden" in request.POST:
            kommentar_form = KommentarForm(request.POST)
            if kommentar_form.is_valid():
                kommentar = kommentar_form.save(commit=False)
                kommentar.aufgabe = aufgabe
                kommentar.autor   = request.user
                kommentar.save()
                messages.success(request, "Kommentar wurde hinzugefügt.")
                return redirect("aufgabe_detail", pk=aufgabe.pk)

        elif "status_speichern" in request.POST:
            status_form = StatusForm(request.POST, instance=aufgabe)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Status wurde aktualisiert.")
                return redirect("aufgabe_detail", pk=aufgabe.pk)

    return render(request, "aufgaben/aufgabe_detail.html", {
        "aufgabe":        aufgabe,
        "kommentare":     aufgabe.kommentare.select_related("autor").all(),
        "kommentar_form": kommentar_form,
        "status_form":    status_form,
    })


@login_required
def aufgabe_erstellen(request, projekt_id=None):
    projekt = None
    if projekt_id:
        projekt = get_object_or_404(Projekt, id=projekt_id)

    if request.method == "POST":
        form = AufgabeForm(
            request.POST,
            aktueller_user=request.user,
            projekt=projekt
        )
        if form.is_valid():
            aufgabe = form.save(commit=False)
            aufgabe.erstellt_von = request.user
            if projekt and not aufgabe.projekt_id:
                aufgabe.projekt = projekt
            aufgabe.save()
            messages.success(request, "Aufgabe wurde erstellt.")
            if aufgabe.projekt:
                return redirect("kanban_board", projekt_id=aufgabe.projekt.id)
            return redirect("aufgabe_detail", pk=aufgabe.pk)
    else:
        initial = {'projekt': projekt_id} if projekt_id else {}
        form = AufgabeForm(
            initial=initial,
            aktueller_user=request.user,
            projekt=projekt
        )

    return render(request, "aufgaben/aufgabe_form.html", {
        "form":        form,
        "seite_titel": "Neue Aufgabe",
        "projekt_id":  projekt_id,
        "projekt":     projekt,
    })


@login_required
def aufgabe_bearbeiten(request, pk):
    aufgabe = get_object_or_404(Aufgabe, pk=pk)

    #  Fix #3: Berechtigungsprüfung
    if not (aufgabe.erstellt_von == request.user or
            (aufgabe.projekt and aufgabe.projekt.admin == request.user)):
        return HttpResponseForbidden("Keine Berechtigung!")

    if request.method == "POST":
        form = AufgabeForm(
            request.POST,
            instance=aufgabe,
            aktueller_user=request.user,
            projekt=aufgabe.projekt
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Aufgabe wurde bearbeitet.")
            return redirect("aufgabe_detail", pk=aufgabe.pk)
    else:
        form = AufgabeForm(
            instance=aufgabe,
            aktueller_user=request.user,
            projekt=aufgabe.projekt
        )

    return render(request, "aufgaben/aufgabe_form.html", {
        "form":        form,
        "seite_titel": "Aufgabe bearbeiten",
        "projekt":     aufgabe.projekt,
        "aufgabe":     aufgabe,
    })


@login_required
def aufgabe_loeschen(request, pk):
    aufgabe    = get_object_or_404(Aufgabe, pk=pk)
    projekt_id = aufgabe.projekt.id if aufgabe.projekt else None

    #  Fix #3: Berechtigungsprüfung


    if request.method == "POST":
        aufgabe.delete()
        messages.success(request, "Aufgabe wurde gelöscht.")
        if projekt_id:
            return redirect("kanban_board", projekt_id=projekt_id)
        return redirect("dashboard")

    return render(request, "aufgaben/aufgabe_confirm_delete.html", {
        "aufgabe": aufgabe
    })
