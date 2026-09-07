from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("initiate/", views.initiate, name="initiate"),
    path("lab/", views.lab, name="lab"),
    path("protocol/", views.protocol, name="protocol"),
    path("clone/<uuid:pk>/", views.clone_detail, name="clone_detail"),
    path("clone/<uuid:pk>/advance/", views.advance, name="advance"),
    path("health/", views.health, name="health"),
]
