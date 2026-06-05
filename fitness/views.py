from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Workout, Set, Exercise
import json
from django.utils import timezone

@login_required
def dashboard(request):
    exercises = Exercise.objects.all()
    
    # if request.method == 'POST':
    #     form = WorkoutForm(request.POST)
    #     if form.is_valid():
    #         try:
    #             form.save()
    #         except AttributeError:
    #             data = form.cleaned_data
    #             workout = Workout.objects.create(name=data.get('name', ''))
    #             sets = data.get('sets')
    #             if sets:
    #                 workout.sets.set(sets)
    #         form = WorkoutForm()
    # else:
    #     form = WorkoutForm()

    return render(request, 'fitness/dashboard.html', {'user': request.user, 'exercises': exercises})



def workout_view(request, workout_id=None):
    # Se non c'è un ID, creiamo il workout (solo la prima volta)
    if not workout_id:
        workout = Workout.objects.create(name=f'Workout di {request.user} - {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
        exercises = []
        all_exercises = Exercise.objects.all()
    else:
        workout = get_object_or_404(Workout, id=workout_id)

    return render(request, 'fitness/workout.html', {'workout': workout, 'exercises': exercises, 'all_exercises': all_exercises})

def save_workout(request, workout_id):
    if request.method == 'POST':
        workout = get_object_or_404(Workout, id=workout_id)
        
        # Recuperiamo le liste inviate dal form HTML
        exercises = request.POST.getlist('exercise_name[]')
        repetitions = request.POST.getlist('repetitions[]')
        weights = request.POST.getlist('weight[]')
        
        # Svuotiamo i set precedenti se stiamo sovrascrivendo (opzionale)
        workout.sets.all().delete()
        
        # Cicliamo i dati per creare gli esercizi e i set
        for name, reps, weight in zip(exercises, repetitions, weights):
            if name.strip(): # Evita di salvare se l'utente ha lasciato una riga vuota
                # Trova l'esercizio o crealo se non esiste nel database
                exercise, _ = Exercise.objects.get_or_create(name=name.strip())
                
                # Crea il set
                new_set = Set.objects.create(
                    exercise=exercise,
                    repetitions=int(reps),
                    weight=float(weight)
                )
                # Associalo al workout
                workout.sets.add(new_set)
        
        # Una volta salvato tutto, torna alla dashboard
        return redirect('dashboard')
        
    return redirect('dashboard')