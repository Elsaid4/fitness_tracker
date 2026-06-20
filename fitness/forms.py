from django import forms
from .models import Workout, Exercise


class WorkoutForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    repetitions = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
