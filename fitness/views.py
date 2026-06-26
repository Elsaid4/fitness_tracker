from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Workout, Set, Exercise, WorkoutExercise
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

@login_required
def dashboard(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-timestamp')
    workout_exercises = []
    sets = []
    for w in workouts:
        workout_exercises.extend(WorkoutExercise.objects.filter(workout=w))

    for we in workout_exercises:
        sets.extend(Set.objects.filter(workout_exercise=we))

    return render(request, 'fitness/dashboard.html', {
        'user': request.user, 
        'workouts': workouts, 
        'exercises': workout_exercises, 
        'sets': sets
        })


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'fitness/workout_detail.html'
    context_object_name = 'workout'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.get_object()
        
        workout_exercises = WorkoutExercise.objects.filter(workout=workout)
        
        sets_by_exercise = {}
        for we in workout_exercises:
            sets_by_exercise[we] = Set.objects.filter(workout_exercise=we)
            
        context['workout_exercises'] = workout_exercises
        context['sets_by_exercise'] = sets_by_exercise
        return context



@login_required
def workout_view(request):
    workout = Workout(name=f'Workout di {request.user} - {timezone.now().strftime("%d-%m-%Y %H:%M:%S")}')
    exercises = []
    all_exercises = Exercise.objects.all()
    total_weight = 0
    

    return render(request, 'fitness/workout.html', {
        'workout': workout, 
        'exercises': exercises, 
        'all_exercises': all_exercises, 
        'tot_weight': total_weight 
    })

@login_required
def save_workout(request, workout_name):
    if request.method == 'POST':
        current_user = request.user
        duration_str = request.POST.get('workout_duration', '00:00:00')
        
        workout = Workout.objects.create(
            name=workout_name, 
            user=current_user,
            duration=duration_str
        )
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
        return redirect('workout_detail', workout_id=workout.id)
    return redirect('dashboard')