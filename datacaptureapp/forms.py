from django import forms
from datacaptureapp.models import Project
from datacaptureapp.models import Profile


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
        }
