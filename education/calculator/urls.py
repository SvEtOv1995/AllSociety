from django.urls import path
from .views import algebra_view, geometry_view
from . import views
from .views import get_entries

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница (запускается сразу)
    path('algebra/', views.algebra_view, name='algebra'),
    path('geometry/', views.geometry_view, name='geometry'),
    path('get_entries/', get_entries, name='get_entries'),

]
