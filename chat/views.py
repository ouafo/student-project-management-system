from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import  ChatNachrichtForm
from .models import ChatNachricht
# Create your views here.
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