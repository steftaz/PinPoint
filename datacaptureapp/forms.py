from django import forms
from datacaptureapp.models import Project, Attribute, Node
from datacaptureapp.models import Profile
from datacaptureapp.models import Project, Attribute, Data, Node


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'is_public']
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


class CreateDataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['value']


class CreateNodeForm(forms.ModelForm):
    picture = forms.ImageField(label='', required=False)

    class Meta:
        model = Node
        fields = ('latitude', 'longitude', 'picture')
        widgets = {
            'latitude': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'latitude', 'name': 'latitude'}),
            'longitude': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'longitude', 'name': 'longitude'})
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


class AddMemberForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'name': "email", 'type': 'text', 'class': 'form-control', 'placeholder': 'e-mail',
               'aria-label': 'email', 'aria-describedby': 'basic-addon1'}))


class ChangePublicPrivateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['is_public']
