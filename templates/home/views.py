from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # speichert User in PostgreSQL
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "home/registrierung.html", {"form": form})
User = get_user_model()

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False          # ❗ Noch nicht einloggen lassen
            user.save()

            # E-Mail-Bestätigung vorbereiten
            current_site = get_current_site(request)
            mail_subject = 'Aktiviere deinen Boardify-Account'
            message = render_to_string('home/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return render(request, "home/check_email.html")
    else:
        form = RegisterForm()
        return render(request, "home/registrierung.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "home/activation_success.html")
    else:
        return render(request, "home/activation_failed.html")