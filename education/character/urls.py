from django.urls import path
from .views import character_status, add_exp

urlpatterns = [
    path("status/", character_status, name="character_status"),
    path("add_exp/<int:amount>/", add_exp, name="add_exp"),
]
