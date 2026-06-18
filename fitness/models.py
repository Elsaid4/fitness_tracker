from django.db import models

class Exercise(models.Model):
    """
    Questo è il catalogo globale degli esercizi (es. Panca Piana, Squat).
    Viene popolato una volta sola (es. con le fixture).
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories_burned_per_minute = models.FloatField()

    def __str__(self):
        return self.name


class Workout(models.Model):
    """
    Rappresenta la singola sessione di allenamento
    """
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.timestamp.strftime('%d/%m/%Y')}"


class WorkoutExercise(models.Model):
    """
    Rappresenta un esercizio specifico inserito all'interno di un determinato Workout.
    """
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"


class Set(models.Model):
    """
    Rappresenta le serie eseguite. Ogni serie è legata a un esercizio dentro a un workout.
    """
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    repetitions = models.IntegerField()
    weight = models.FloatField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.repetitions} reps @ {self.weight}kg"