from django import forms
from datacaptureapp.models import Project
from datacaptureapp.models import Profile
from datacaptureapp.models import Project, Attribute


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }


class CreateAttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        fields = ['name', 'type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter attribute name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=(('text', 'Text'), ('number', 'Number')))
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
