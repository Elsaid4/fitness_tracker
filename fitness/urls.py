from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workout/', views.workout_view, name='workout'),
    path('workout/save_workout/<str:workout_name>/', views.save_workout, name='save_workout'),
    path('workout_detail/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('coach_list/', views.CoachListView.as_view(), name='coach_list'),
    path('coach_detail/<int:pk>', views.CoachDetailView.as_view(), name='coach_detail'),
    path('coach/<int:coach_id>/toggle-follow/', views.toggle_follow_view, name='toggle_follow'),
]