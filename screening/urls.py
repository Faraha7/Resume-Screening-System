from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

class LogoutViewGET(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('results/', views.top_candidates, name='top_candidates'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('accounts/logout/', LogoutViewGET.as_view(next_page='/upload/'), name='logout'),
]
