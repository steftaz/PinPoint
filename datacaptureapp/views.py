from django.http import FileResponse, QueryDict, HttpResponse
from django.shortcuts import render, redirect
from datacaptureapp.forms import *
from datacaptureapp.models import *
from account.models import Account as UserAccount
from datacaptureapp.export_builder import *
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from decimal import Decimal


@login_required()
def projects(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    return render(request, 'datacaptureapp/home.html', {'projects': projects, 'user': user})


@login_required()
def newproject(request):
    if request.method == 'POST':
        user = request.user
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            creator = UserAccount.objects.filter(email=user.email).first()
            new_project.user.add(creator)
            return redirect('attributes', new_project.id)
    else:
        form = CreateProjectForm
        return render(request, "datacaptureapp/NewProject.html", {'form': form})


@login_required()
def project(request, pk=0):
    if pk == 0:
        return render(request, 'datacaptureapp/home.html')
    geojson = generate_geojson(pk)
    requested_project = Project.objects.filter(id=pk).first()
    owner = requested_project.user.all().first()
    return render(request, 'datacaptureapp/Project.html',
                  {'project': requested_project, 'owner': owner, 'geojson': geojson})


@login_required()
def addnode(request, pk):
    requested_project = Project.objects.filter(id=pk).first()
    attributes = Attribute.objects.filter(project=requested_project)
    if request.method == "POST":
        latitude_formatted = "{:.8f}".format(Decimal(request.POST.get('latitude')))
        longitude_formatted = "{:.8f}".format(Decimal(request.POST.get('longitude')))
        node_query_dict = QueryDict('latitude=' + latitude_formatted + '&' + 'longitude=' + longitude_formatted)
        node_form = CreateNodeForm(node_query_dict)
        if node_form.is_valid():
            node = node_form.save(commit=False)
            node.project = requested_project
            node.save()
        for attribute in attributes:
            data_query_dict = QueryDict('value=' + request.POST.get(attribute.name))
            data_form = CreateDataForm(data_query_dict)
            if data_form.is_valid():
                data = data_form.save(commit=False)
                data.node = node
                data.attribute = attribute
                data.save()
        return redirect('project', pk)
    form = CreateDataForm()
    del form.fields['value']
    for attribute in attributes:
        form.fields[attribute.name] = forms.DecimalField() if attribute.type == "number" else forms.CharField()
    return render(request, 'datacaptureapp/AddFeature.html', {'form': form, 'project_id': pk})


@login_required()
def nodes(request, pk):
    if request.method == 'POST':
        data_type = request.POST.get('data_type')
        if data_type == 'CSV':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(Project.objects.filter(id=pk).first().name)
            generate_csv(response, pk)
        elif data_type == 'GeoJSON':
            geojson = generate_geojson(pk)
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="{}.geojson"'.format(json.loads(geojson)['name'])
            response.write(geojson)
        return response
    attributes = Attribute.objects.filter(project__id=pk)
    data = Data.objects.filter(attribute__in=attributes)
    requested_nodes = Node.objects.filter(project_id=pk)
    overview = {}
    for node in requested_nodes:
        overview[node.pk] = {'latitude': node.latitude, 'longitude': node.longitude}
        for data_object in data:
            if data_object.node == node:
                overview[node.pk][data_object.attribute.name] = data_object.value
    return render(request, 'datacaptureapp/FeatureOverview.html', {'overview': overview, 'attributes': attributes})


@login_required()
def add_attribute(request, pk):
    if request.method == 'POST':
        form = CreateAttributeForm(request.POST)
        if form.is_valid():
            new_attribute = form.save(commit=False)
            project = Project.objects.filter(id=pk).first()
            new_attribute.project = project
            new_attribute.save()
            return redirect('attributes', pk)
    else:
        form = CreateAttributeForm
        return render(request, 'datacaptureapp/FormCreation.html', {'form': form})


@login_required()
def formcreation(request):
    return render(request, 'datacaptureapp/FormCreation.html', {})


@login_required()
def logout_view(request):
    logout(request)
    return redirect("/login/")


@login_required()
def profile(request):
    return render(request, 'datacaptureapp/Profile.html', {})


@login_required()
def newprofile(request):
    return render(request, 'datacaptureapp/NewProfile.html', {})

@login_required()
def editprofile(request):
    return render(request, 'datacaptureapp/EditProfile.html', {})
