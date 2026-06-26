from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workout/', views.workout_view, name='workout'),
    path('workout/save_workout/<str:workout_name>/', views.save_workout, name='save_workout'),
    path('workout_detail/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
]