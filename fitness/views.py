from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Exercise, Workout
from .forms import WorkoutForm

@login_required
def dashboard(request):
    exercises = Exercise.objects.all()
    
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except AttributeError:
                # Fallback: crea manualmente l'istanza se il ModelForm non espone save()
                data = form.cleaned_data
                workout = Workout.objects.create(name=data.get('name', ''))
                sets = data.get('sets')
                if sets:
                    workout.sets.set(sets)
            form = WorkoutForm()
    else:
        form = WorkoutForm()

    return render(request, 'fitness/dashboard.html', {'user': request.user, 'exercises': exercises, 'form': form})

