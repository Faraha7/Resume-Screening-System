from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('screening.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset
    path('', RedirectView.as_view(url='/upload/', permanent=False)),
]
