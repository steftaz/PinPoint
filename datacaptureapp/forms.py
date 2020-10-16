from django import forms
from datacaptureapp.models import Project, Attribute, Node
from datacaptureapp.models import Profile
from datacaptureapp.models import Project, Attribute, Data, Node



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



class CreateDataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = []
    # class Meta:
    #     model = Node
    #     fields = ['latitude', 'longitude']
    #     widgets = {
    #         'latitude': forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}),
    #         'longitude': forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'})
    #     }
    # latitude = forms.DecimalField(decimal_places=8, max_digits=10)
    # longitude = forms.DecimalField(decimal_places=8, max_digits=11)

    def __init__(self, *args, **kwargs):
        super(CreateDataForm, self).__init__(*args, **kwargs)
        if args:
            for field in args:
                self.fields[field] = forms.CharField(widget=forms.TextInput)
        elif kwargs:
            data = kwargs
            del data['latitude']
            del data['longitude']

            fields = list(data.keys())
            for field in fields:
                self.fields[field] = forms.CharField(widget=forms.TextInput)

    def get_fields(self):
        for field_name in self.fields:
            yield self[field_name]


class CreateNodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ('latitude', 'longitude')







class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
        }

