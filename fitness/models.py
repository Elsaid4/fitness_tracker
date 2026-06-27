from django.db import models
from django.conf import settings

from accounts.models import CustomUser

class Exercise(models.Model):
    """
    Questo è il catalogo globale degli esercizi (es. Panca Piana, Squat).
    Viene popolato una volta sola (es. con le fixture).
    """
    name                        = models.CharField(max_length=100)
    description                 = models.TextField()
    calories_burned_per_minute  = models.FloatField()

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    coach       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Coach: {self.coach.username})"

class Workout(models.Model):
    """
    Rappresenta la singola sessione di allenamento
    """
    name            = models.CharField(max_length=100)
    timestamp       = models.DateTimeField(auto_now_add=True)
    duration        = models.CharField(max_length=8, default="00:00:00")
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='workouts')
    plan            = models.ForeignKey(TrainingPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='workouts')
    is_template     = models.BooleanField(default=False)
    parent_workout  = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        user_part = f" by {self.user}" if self.user else ""
        duration_part = f" ({self.duration})" if self.duration else ""
        return f"{self.name} - {self.timestamp.strftime('%d/%m/%Y')}{user_part}"


class WorkoutExercise(models.Model):
    """
    Rappresenta un esercizio specifico inserito all'interno di un determinato Workout.
    """
    workout     = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise    = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"


class Set(models.Model):
    """
    Rappresenta le serie eseguite. Ogni serie è legata a un esercizio dentro a un workout.
    """
    workout_exercise    = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    repetitions         = models.IntegerField()
    weight              = models.FloatField()
    completed           = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.repetitions} reps @ {self.weight}kg"
    
class WorkoutFeedback(models.Model):
    """
    Tabella per i feedback dei coach 
    """
    workout     = models.OneToOneField(Workout, on_delete=models.CASCADE, related_name='feedback')
    coach       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment     = models.TextField()
    rating      = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

