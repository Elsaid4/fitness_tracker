from django.db import models

# Create your models here.

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories_burned_per_minute = models.FloatField()

    def __str__(self):
        return self.name

class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.repetitions} reps of {self.exercise.name} at {self.weight} kg"

class Workout(models.Model):
    name = models.CharField(max_length=100)
    sets = models.ManyToManyField(Set)

    def __str__(self):
        return self.name
