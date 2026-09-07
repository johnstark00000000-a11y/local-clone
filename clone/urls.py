from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_profile, name="create"),
    path("lab/", views.lab, name="lab"),
    path("p/<uuid:pk>/", views.dashboard, name="dashboard"),
    path("p/<uuid:pk>/chat/", views.chat, name="chat"),
    path("p/<uuid:pk>/upload/", views.upload_view, name="upload"),
    path("p/<uuid:pk>/future/", views.future_view, name="future"),
    path("health/", views.health, name="health"),
]
