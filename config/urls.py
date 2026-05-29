from django.contrib import admin
from django.urls import include, path
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", accounts_views.startseite, name="startseite"),
    path('', include('accounts.urls')),
    path('projekte/', include('projekte.urls')),
    path('aufgaben/', include('aufgaben.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]