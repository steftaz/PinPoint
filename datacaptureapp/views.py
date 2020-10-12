from django.shortcuts import render
from datacaptureapp.forms import *
from datacaptureapp.models import *

def home(request):
  return render(request, 'datacaptureapp/home.html', {})

def create_project(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['project_name']
            project.description = form.cleaned_data['project_description']
            project.user = request.user
            project.save()
            return render(request, "datacaptureapp/NewProject.html")
        else:
            return render(request, "datacaptureapp/NewProject.html")

def newproject(request):
    return render(request, 'datacaptureapp/NewProject.html', {})

def project(request):
    return render(request, 'datacaptureapp/Project.html',{})

def addfeature(request):
    return render(request, 'datacaptureapp/AddFeature.html', {})

def featureoverview(request):
    return render(request, 'datacaptureapp/FeatureOverview.html', {})

def formcreation(request):
    return render(request, 'datacaptureapp/FormCreation.html', {})

