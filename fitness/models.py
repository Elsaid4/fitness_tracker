from django.db import models

# Create your models here.

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories_burned_per_minute = models.FloatField()
    sets = models.ManyToManyField('Set', related_name='exercises')
    workouts = models.ManyToManyField('Workout', related_name='exercises')

    def __str__(self):
        return self.name

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField()
    weight = models.FloatField()
    duration = models.TimeField(default='00:00:00')
    # workout = models.ForeignKey('Workout', on_delete=models.CASCADE, related_name='sets')

    def __str__(self):
        return f"{self.repetitions} reps of {self.exercise.name} at {self.weight} kg"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
