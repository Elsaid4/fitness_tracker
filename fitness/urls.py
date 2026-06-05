from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workout/', views.workout_view, name='workout'),
    path('workout/save_workout/<int:workout_id>/', views.save_workout, name='save_workout'),
]