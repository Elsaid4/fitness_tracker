from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class ProfileForm(forms.ModelForm): 
    class Meta:
        model = Profile
        fields = ['name', 'last_name', 'bio', 'address', 'phone_number', 'weight', 'height', 'age']
        
        labels = {
            'name': 'Nome',
            'last_name': 'Cognome',
            'bio': 'Biografia / Note',
            'address': 'Indirizzo',
            'phone_number': 'Numero di Telefono',
            'weight': 'Peso attuale (kg)',
            'height': 'Altezza (cm)',
            'age': 'Età',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Inserisci il tuo cognome'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Racconta qualcosa di te...', 'rows': 3}),
            'address': forms.TextInput(attrs={'placeholder': 'Via Roma 10'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '3331234567'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})