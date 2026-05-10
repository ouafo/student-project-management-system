from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AufgabeForm, KommentarForm, StatusForm
from .models import Aufgabe


@login_required
def kanban_board(request):
    context = {
        "offen": Aufgabe.objects.filter(status=Aufgabe.Status.OFFEN).select_related("zugewiesen_an"),
        "in_bearbeitung": Aufgabe.objects.filter(status=Aufgabe.Status.IN_BEARBEITUNG).select_related("zugewiesen_an"),
        "in_ueberpruefung": Aufgabe.objects.filter(status=Aufgabe.Status.IN_UEBERPRUEFUNG).select_related("zugewiesen_an"),
        "erledigt": Aufgabe.objects.filter(status=Aufgabe.Status.ERLEDIGT).select_related("zugewiesen_an"),
    }
    return render(request, "aufgaben/kanban_board.html", context)


@login_required
def aufgabe_detail(request, pk):
    aufgabe = get_object_or_404(
        Aufgabe.objects.select_related("zugewiesen_an", "erstellt_von").prefetch_related("kommentare__autor"),
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
                return redirect("aufgaben:aufgabe_detail", pk=aufgabe.pk)

        elif "status_speichern" in request.POST:
            status_form = StatusForm(request.POST, instance=aufgabe)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, "Status wurde aktualisiert.")
                return redirect("aufgaben:aufgabe_detail", pk=aufgabe.pk)

    context = {
        "aufgabe": aufgabe,
        "kommentare": aufgabe.kommentare.select_related("autor").all(),
        "kommentar_form": kommentar_form,
        "status_form": status_form,
    }
    return render(request, "aufgaben/aufgabe_detail.html", context)


@login_required
def aufgabe_erstellen(request):
    if request.method == "POST":
        form = AufgabeForm(request.POST)
        if form.is_valid():
            aufgabe = form.save(commit=False)
            aufgabe.erstellt_von = request.user
            aufgabe.save()
            messages.success(request, "Aufgabe wurde erstellt.")
            return redirect("aufgaben:aufgabe_detail", pk=aufgabe.pk)
    else:
        form = AufgabeForm()

    return render(request, "aufgaben/aufgabe_form.html", {"form": form, "seite_titel": "Neue Aufgabe"})


@login_required
def aufgabe_bearbeiten(request, pk):
    aufgabe = get_object_or_404(Aufgabe, pk=pk)

    if request.method == "POST":
        form = AufgabeForm(request.POST, instance=aufgabe)
        if form.is_valid():
            form.save()
            messages.success(request, "Aufgabe wurde bearbeitet.")
            return redirect("aufgaben:aufgabe_detail", pk=aufgabe.pk)
    else:
        form = AufgabeForm(instance=aufgabe)

    return render(request, "aufgaben/aufgabe_form.html", {"form": form, "seite_titel": "Aufgabe bearbeiten"})


@login_required
def aufgabe_loeschen(request, pk):
    aufgabe = get_object_or_404(Aufgabe, pk=pk)

    if request.method == "POST":
        aufgabe.delete()
        messages.success(request, "Aufgabe wurde gelöscht.")
        return redirect("aufgaben:kanban_board")

    return render(request, "aufgaben/aufgabe_confirm_delete.html", {"aufgabe": aufgabe})