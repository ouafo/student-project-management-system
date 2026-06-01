from django.contrib import admin
from django.contrib.auth.context_processors import auth
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from projekte import views as projekt_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.startseite, name='startseite'),
    path('dashboard/', projekt_views.dashboard_view, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('projekte/', include('projekte.urls')),
    path('aufgaben/', include('aufgaben.urls')),
    path('kanban/', include('kanban.urls')),
    path('kommentare/', include('kommentare.urls')),
    path('chat/', include('chat.urls')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)