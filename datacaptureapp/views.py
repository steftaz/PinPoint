from django.shortcuts import render
from datacaptureapp.forms import *
from datacaptureapp.models import *
from account.models import Account as UserAccount


def home(request):
    return render(request, 'datacaptureapp/home.html', {})


def newproject(request):
    if request.method == 'POST':
        user = request.user
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            creator = UserAccount.objects.filter(email=user.email).first()
            new_project.user.add(creator)
            return render(request, "datacaptureapp/home.html")
    else:
        form = CreateProjectForm
        return render(request, "datacaptureapp/NewProject.html", {'form': form})


def project(request):
    requested_project = Project.objects.filter(id=request.GET['project_id']).first()
    owner = requested_project.user.all().first()
    return render(request, 'datacaptureapp/Project.html', {'project': requested_project, 'owner': owner})


def addfeature(request):
    return render(request, 'datacaptureapp/AddFeature.html', {})


def featureoverview(request):
    return render(request, 'datacaptureapp/FeatureOverview.html', {})


def add_attribute(request):
    if request.method == 'POST':
        user = request.user
    else:
        form = CreateAttributeForm
        return render(request, 'datacaptureapp/FormCreation.html', {'form': form})
