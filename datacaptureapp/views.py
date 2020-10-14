from django.http import FileResponse
from django.shortcuts import render
from datacaptureapp.forms import *
from datacaptureapp.models import *
from account.models import Account as UserAccount
from datacaptureapp.GeoJsonBuilder import *


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
            form = CreateProjectForm()
            return render(request, "datacaptureapp/home.html", {'form': form})
    else:
        form = CreateProjectForm
        return render(request, "datacaptureapp/NewProject.html", {'form': form})


def project(request):
    if request.method == 'POST':
        #TODO Get correct project id out  of request
        id = 1

        project = generate_geojson(id)
        file_path = "datacaptureapp/tmp/" + project.split("\"")[3] + ".geojson"
        file = open(file_path, "w")
        file.write(project)
        file.close()
        return FileResponse(open(file_path, 'rb'))

        # TODO Remove new file (os.remove throws an error)
    else:
        return render(request, 'datacaptureapp/Project.html', {})


def addfeature(request):
    return render(request, 'datacaptureapp/AddFeature.html', {})


def featureoverview(request):
    return render(request, 'datacaptureapp/FeatureOverview.html', {})


def formcreation(request):
    return render(request, 'datacaptureapp/FormCreation.html', {})


