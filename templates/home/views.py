from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # speichert User in PostgreSQL
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "home/registrierung.html", {"form": form})
