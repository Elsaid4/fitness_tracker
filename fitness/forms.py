from django import forms
from .models import TrainingPlan, Workout, Exercise
from django.forms import inlineformset_factory


class WorkoutForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    repetitions = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['name', 'description']
        labels = {
            'name': 'Nome della Scheda / Programma',
            'description': 'Descrizione o Note per gli atleti',
        }
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

WorkoutInlineFormSet = inlineformset_factory(
    TrainingPlan, 
    Workout,
    fields=['name'], # Al coach facciamo inserire solo il nome del workout
    labels={'name': 'Nome del Workout (Giorno)'},
    widgets={'name': forms.TextInput(attrs={'placeholder': 'Es: Giorno A - Spinta', 'class': 'form-control'})},
    extra=4, # Mostra fino a 4 workout inseribili contemporaneamente
    can_delete=False # Non serve la cancellazione in fase di prima creazione
)