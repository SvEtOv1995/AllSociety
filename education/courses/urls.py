from django.urls import path
from . import views
from .views import save_board_data, get_board_data

urlpatterns = [
    path('', views.subjects_list, name='subjects_list'),
    path('subject/<int:subject_id>/', views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('check_answer/<int:question_id>/', views.check_answer, name='check_answer'),
    path('subject/<int:subject_id>/calculator/', views.subject_calculator, name='subject_calculator'),
    path('subject/<int:subject_id>/notes/', views.subject_notes, name='subject_notes'),
    path('lesson/<int:lesson_id>/get_board_data/', views.get_board_data, name='get_board_data'),
    path('lesson/<int:lesson_id>/save_board_data/', views.save_board_data, name='save_board_data'),
]

