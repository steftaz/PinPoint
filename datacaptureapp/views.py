from django.core.exceptions import PermissionDenied
from django.http import QueryDict, HttpResponse, JsonResponse
from django.core import serializers
from django.http import FileResponse, QueryDict, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from datacaptureapp.forms import *
from datacaptureapp.models import *
from account.models import Account as UserAccount
from datacaptureapp.export_builder import *
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from decimal import Decimal
from django.contrib import messages


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
    requested_project = Project.objects.filter(id=pk).first()
    if not requested_project:
        if request.headers.get('search-by-id'):
            messages.error(request, 'The project you were looking for does not exist')
            return JsonResponse({"messages": messagesToList(request)})
        else:
            raise PermissionDenied
    else:
        if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
            # POST request to change private/public
            if request.POST:
                form = ChangePublicPrivateForm(request.POST, instance=requested_project)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'is_public': requested_project.is_public})
            else:
                if request.headers.get('search-by-id'):
                    return JsonResponse({'url': '/projects/' + str(pk) + '/'})
                else:
                    geojson = generate_geojson(pk)
                    owner = requested_project.user.all().first()  # TODO there are more users now, we do not specify the owner
                    attributes = Attribute.objects.filter(project__id=pk)
                    data = Data.objects.filter(attribute__in=attributes)
                    requested_nodes = Node.objects.filter(project_id=pk)
                    overview = get_node_overview(data, requested_nodes)
                    return render(request, 'datacaptureapp/Project.html',
                                  {'project': requested_project, 'owner': owner, 'geojson': geojson,
                                   'overview': overview, 'data': data, 'attributes': attributes,
                                   'requested_nodes': requested_nodes})
        else:
            if request.headers.get('search-by-id'):
                messages.error(request, 'This project is private. Ask the project owner to add you to this project.')
                return JsonResponse({"messages": messagesToList(request)})
            else:
                raise PermissionDenied



def get_node_overview(data, requested_nodes):
    overview = {}
    for node in requested_nodes:
        overview[node.pk] = {'latitude': node.latitude, 'longitude': node.longitude}
        for data_object in data:
            if data_object.node == node:
                overview[node.pk][data_object.attribute.name] = data_object.value
    return overview



@login_required()
def addnode(request, pk):
    requested_project = get_object_or_404(Project, pk=pk)
    #requested_project = Project.objects.filter(id=pk).first()
    if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
        attributes = Attribute.objects.filter(project=requested_project)
        if request.method == "POST":
            latitude_formatted = "{:.8f}".format(Decimal(request.POST.get('latitude')))
            longitude_formatted = "{:.8f}".format(Decimal(request.POST.get('longitude')))
            request.POST._mutable = True
            request.POST['latitude'] = latitude_formatted
            request.POST['longitude'] = longitude_formatted
            request.POST._mutable = False
            node_form = CreateNodeForm(request.POST, request.FILES)

            if node_form.is_valid():
                node = node_form.save(commit=False)
                node.project = requested_project
                node.save()

            for attribute in attributes:
                data_query_dict = QueryDict('value=' + request.POST.get(attribute.name))
                data_form = CreateDataForm(data_query_dict)
                if not data_form.is_valid():
                    data_form = CreateDataForm(QueryDict("value=Null"))
                data = data_form.save(commit=False)
                data.node = node
                data.attribute = attribute
                data.save()
            return redirect('project', pk)
        else:
            node_form = CreateNodeForm()
            datas = []
            for attribute in attributes:
                data = CreateDataForm(QueryDict('value=Null'))
                data = data.save(commit=False)
                data.attribute = attribute
                datas.append(data)
            return render(request, 'datacaptureapp/AddFeature.html', {'node_form': node_form, 'datas': datas, 'project_id': pk})
    else:
        raise PermissionDenied


@login_required()
def nodes(request, pk):
    requested_project = get_object_or_404(Project, pk=pk)
    if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
        if request.method == 'POST':
            post = request.POST
            if 'data_type' in post:
                data_type = request.POST.get('data_type')
                if data_type == 'CSV':
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(requested_project.name)
                    generate_csv(response, pk)
                elif data_type == 'GeoJSON':
                    geojson = generate_geojson(pk)
                    response = HttpResponse(content_type='application/json')
                    response['Content-Disposition'] = 'attachment; filename="{}.geojson"'.format(json.loads(geojson)['name'])
                    response.write(geojson)
                return response
            elif 'remove_node' in post:
                Node.objects.get(id=post['remove_node']).delete()
        else:
            attributes = Attribute.objects.filter(project__id=pk)
            data = Data.objects.filter(attribute__in=attributes)
            requested_nodes = Node.objects.filter(project_id=pk)
            overview = get_node_overview(data, requested_nodes)
            images = {}
            for node in requested_nodes:
                images[node.pk] = node.picture
            return render(request, 'datacaptureapp/FeatureOverview.html',
                          {'overview': overview, 'images': images, 'attributes': attributes})
    else:
        raise PermissionDenied



@login_required()
def edit_node(request, pk, nk):
    requested_project = get_object_or_404(Project, pk=pk)
    node = get_object_or_404(Node, id=nk)
    if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
        if request.method == 'POST':
            post = request.POST
            for coor in ['longitude', 'latitude']:
                value = post[coor]
                if value != '':
                    node.coor = value
            if 'picture' in request.FILES:
                node.picture = request.FILES['picture']
            node.save()
            attributes = Attribute.objects.filter(project=Project.objects.get(id=pk))
            for attribute in attributes:
                value = post[attribute.name]
                if value != '':
                    data = Data.objects.get(node=node, attribute=attribute)
                    data.value = value
                    data.save()
            return redirect('nodes', pk)
        node = Node.objects.get(id=nk)
        datas = Data.objects.filter(node=node)
        return render(request, 'datacaptureapp/EditNode.html', {'node': node, 'datas': datas})
    else:
        raise PermissionDenied



@login_required()
def add_attribute(request, pk):
    requested_project = get_object_or_404(Project, pk=pk)
    if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
        if request.method == 'POST':
            form = CreateAttributeForm(request.POST)
            if form.is_valid():
                new_attribute = form.save(commit=False)
                new_attribute.project = requested_project
                new_attribute.save()
                return redirect('attributes', pk)
        else:
            form = CreateAttributeForm
            return render(request, 'datacaptureapp/FormCreation.html', {'form': form})
    else:
        raise PermissionDenied


@login_required()
def messagesToList(request):
    django_messages = []
    for message in messages.get_messages(request):
        django_messages.append({
            "level": message.level,
            "message": message.message,
            "extra_tags": message.tags,
        })
    return django_messages


@login_required()
def team(request, pk):
    requested_project = get_object_or_404(Project, pk=pk)
    if requested_project.user.filter(email=request.user.email).first():
        team_members = requested_project.user.all()
        if request.POST:
            form = AddMemberForm(request.POST)
            if form.is_valid():
                if Account.objects.filter(email=request.POST.get('email')).exists():
                    account = Account.objects.filter(email=form.cleaned_data.get('email')).first()
                    requested_project.user.add(account)
                    messages.success(request, 'Successfully added the user to this project')
                    return JsonResponse({"messages": messagesToList(request), 'email': account.email,
                                         'username': account.username})
                else:
                    messages.error(request, 'Adding team member failed: no user found with that email')
                    return JsonResponse({"messages": messagesToList(request)})

        else:
            form = AddMemberForm()
            return render(request, 'datacaptureapp/ProjectTeam.html',
                          {'form': form, 'team': team_members, 'project': requested_project})
    else:
        raise PermissionDenied


def formcreation(request):
    return render(request, 'datacaptureapp/FormCreation.html', {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user, username, password)
        if user is not None:
            login(request, user)
            return redirect("/projects/")
    return render(request, 'datacaptureapp/Login.html')


@login_required()
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required()
def profile(request):
    return render(request, 'datacaptureapp/Profile.html', {})


@login_required()
def newprofile(request):
    return render(request, 'datacaptureapp/NewProfile.html', {})


@login_required()
def editprofile(request):
    return render(request, 'datacaptureapp/EditProfile.html', {})


def about(request):
    return render(request, 'datacaptureapp/About.html', {})


def faq(request):
    return render(request, 'datacaptureapp/FAQ.html', {})
