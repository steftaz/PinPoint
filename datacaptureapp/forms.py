from django import forms

class CreateProjectForm(forms.Form):
    project_name = forms.CharField(max_length=50, label='Project Name')
    project_description = forms.CharField(widget=forms.Textarea, label='Description')
