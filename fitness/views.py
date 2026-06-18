from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Workout, Set, Exercise, WorkoutExercise
import json
from django.utils import timezone

@login_required
def dashboard(request):
    exercises = Exercise.objects.all()

    return render(request, 'fitness/dashboard.html', {'user': request.user, 'exercises': exercises})



def workout_view(request):
    # Se non c'è un ID, creiamo il workout (solo la prima volta)
    # workout = Workout.objects.create(name=f'Workout di {request.user} - {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
    workout = Workout(name=f'Workout di {request.user} - {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
    exercises = []
    all_exercises = Exercise.objects.all()

    return render(request, 'fitness/workout.html', {'workout': workout, 'exercises': exercises, 'all_exercises': all_exercises})


def save_workout(request, workout_name):
    workout = Workout.objects.create(name=workout_name)
    
    # Esempio: se nel POST ricevi dati strutturati
    # Ottieni tutti gli indici degli esercizi inviati
    exercise_indices = [k.split('_')[1] for k in request.POST.keys() if '_name' in k]

    for i in exercise_indices:
        exercise_name = request.POST.get(f'exercise_{i}_name')
        exercise_obj = Exercise.objects.get(name=exercise_name)
        
        workout_exercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise_obj)
        
        reps_list       = request.POST.getlist(f'exercise_{i}_reps[]')
        weights_list    = request.POST.getlist(f'exercise_{i}_weight[]')
        completed_list  = request.POST.getlist(f'exercise_{i}_completed[]')
        
        for reps, weight, completed in zip(reps_list, weights_list, completed_list):
            is_completed = completed == "true"
            Set.objects.create(
                workout_exercise    = workout_exercise,
                repetitions         = reps,
                weight              = weight,
                completed           = is_completed
            )
    return redirect('dashboard')