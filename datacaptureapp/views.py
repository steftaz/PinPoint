from django.http import FileResponse, QueryDict
from django.shortcuts import render, redirect
from datacaptureapp.forms import *
from datacaptureapp.models import *
from account.models import Account as UserAccount
from datacaptureapp.GeoJsonBuilder import *
from django import forms


def projects(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    return render(request, 'datacaptureapp/home.html', {'projects': projects})

def newproject(request):
    if request.method == 'POST':
        user = request.user
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            creator = UserAccount.objects.filter(email=user.email).first()
            new_project.user.add(creator)
            return redirect('../{}/attributes/'.format(new_project.id))
    else:
        form = CreateProjectForm
        return render(request, "datacaptureapp/NewProject.html", {'form': form})


def project(request, pk=0):
    if pk == 0:
        return render(request, 'datacaptureapp/home.html')
    if request.method == 'POST':
        project = generate_geojson(pk)
        file_path = "datacaptureapp/tmp/" + json.loads(project)['name'] + ".geojson"
        file = open(file_path, "w")
        file.write(project)
        file.close()
        return FileResponse(open(file_path, 'rb'))  # TODO Remove new file (os.remove throws an error)
    else:
        requested_project = Project.objects.filter(id=pk).first()
        geojson = generate_geojson(pk)
        owner = requested_project.user.all().first()
        return render(request, 'datacaptureapp/Project.html', {'project': requested_project, 'owner': owner, 'geojson': geojson})


def addnode(request, pk):
    requested_project = Project.objects.filter(id=pk).first()
    attributes = Attribute.objects.filter(project=requested_project)
    if request.method == "POST":
        node = Node.objects.filter(project=requested_project).first()  # TODO create correct node attribute
        token = str(request.POST.get('csrfmiddlewaretoken'))
        for attribute in attributes:
            post = QueryDict('csrfmiddlewaretoken={}&Value={}'.format(token, request.POST.get(attribute.name)))
            form = CreateDataForm(post)
            if form.is_valid():
                form = form.save(commit=False)
                form.node = node
                form.attribute = Attribute.objects.filter(project=requested_project, name=attribute.name).first()
                form.save()
        return redirect('project', pk)
    else:
        form = CreateDataForm()
        for attribute in attributes:
            if attribute.type == "text":
                type = forms.CharField()
            else:
                type = forms.DecimalField()
            form.fields[attribute.name] = type
        return render(request, 'datacaptureapp/AddFeature.html', {'form': form, 'project_id': pk})


def nodes(request):
    return render(request, 'datacaptureapp/FeatureOverview.html', {})


def add_attribute(request, pk):
    if request.method == 'POST':
        form = CreateAttributeForm(request.POST)
        if form.is_valid():
            new_attribute = form.save(commit=False)
            project = Project.objects.filter(id=pk).first()
            new_attribute.project = project
            new_attribute.save()
            return redirect('../attributes/')
    else:
        form = CreateAttributeForm
        return render(request, 'datacaptureapp/FormCreation.html', {'form': form})

def formcreation(request):
    return render(request, 'datacaptureapp/FormCreation.html', {})

def login(request):
    return render(request, 'datacaptureapp/Login.html', {})

def profile(request):
    return render(request, 'datacaptureapp/Profile.html', {})

def newprofile(request):
    return render(request, 'datacaptureapp/NewProfile.html', {})


