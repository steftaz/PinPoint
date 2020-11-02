from django.core.exceptions import PermissionDenied
from django.shortcuts import  get_object_or_404
from django.http import QueryDict, HttpResponse, JsonResponse, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from datacaptureapp.forms import *
from account.models import Account as UserAccount
from datacaptureapp.export_builder import *
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages


@login_required()
def home(request):
    """
    Renders the home page with all projects of the user and the user as context
    Context variables: projects, user
    :param request: The incoming request
    :return: A render to the home page
    """
    user = request.user
    projects = Project.objects.filter(user=user)
    return render(request, 'datacaptureapp/home.html', {'projects': projects, 'user': user})


@login_required()
def newproject(request):
    """
    Shows a page with a project form in it's context.
    If a POST request is sent, it saves the new project to the database and
    redirects to a page where new attributes can be added
    Context variables: form
    :param request: The incoming request
    :return: A render to the new project page, or a redirect to the adding attributes page
    """
    if request.method == 'POST':
        user = request.user
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            creator = UserAccount.objects.filter(email=user.email).first()
            new_project.user.add(creator)
            request = QueryDict()
            request.method = "GET"
            return redirect('attributes', new_project.id)
    form = CreateProjectForm
    return render(request, "datacaptureapp/NewProject.html", {'form': form})


@login_required()
def project(request, pk=0):
    """
    First checks whether the requested project exists, otherwise throws a 404
    or notifies the requesting page that this project does not exist.
    Then check whether the user is allowed to access this project. If so, render the project page with the necesary parameters.
    Context variables: project, owner, overview, data, attributes, is_owner
    :param request: The incoming request
    :param pk: The id of the project
    :return: A JsonResponse for the search-by-id or a render to the project page
    """
    requested_project = Project.objects.filter(id=pk).first()
    if not requested_project:
        if request.headers.get('search-by-id'):
            messages.error(request, 'The project you were looking for does not exist')
            return JsonResponse({"messages": messagesToList(request)})
        else:
            raise Http404
    else:
        if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
            # POST request to change private/public
            if request.POST:
                form = ChangePublicPrivateForm(request.POST, instance=requested_project) # TODO this is not on this pagy anymore right?
                if form.is_valid():
                    form.save()
                    return JsonResponse({'is_public': requested_project.is_public})
            else:
                if request.headers.get('search-by-id'):
                    return JsonResponse({'url': '/projects/{}/'.format(pk)})
                else:
                    owner = requested_project.user.all().first()  # TODO there are more users now, we do not specify the owner
                    attributes = Attribute.objects.filter(project__id=pk)
                    data = Data.objects.filter(attribute__in=attributes)
                    requested_nodes = Node.objects.filter(project_id=pk)
                    overview = get_node_overview(data, requested_nodes)
                    return render(request, 'datacaptureapp/Project.html', {'project': requested_project, 'owner': owner,
                                   'overview': overview, 'data': data, 'attributes': attributes, 'is_owner': owner == request.user})
        else:
            if request.headers.get('search-by-id'):
                messages.error(request, 'This project is private. Ask the project owner to add you to this project.')
                return JsonResponse({"messages": messagesToList(request)})
            else:
                raise PermissionDenied


@login_required()
def edit_project(request, pk):
    """
    Renders the edit-project page with a the project, so the name and description can be used as placeholders.
    In a POST request the project is either edited or deleted.
    Only the project owner can access this page
    Context variables: project
    :param request: The incoming request
    :param pk: The id of the project
    :return: A render to the edit-project page or a redirect to the home or project page.
    """
    post = request.POST
    requested_project = get_object_or_404(Project, pk=pk)
    if requested_project.user.filter(email=request.user.email).first():
        if post:
            if "remove_project" in request.POST:
                requested_project.delete()
                return redirect('home')
            else:
                requested_project.name = post['name']
                requested_project.description = post['description']
                requested_project.save()
                return redirect('project', pk)
        else:
            return render(request, 'datacaptureapp/Edit_Project.html', {'project': requested_project})
    else:
        raise PermissionDenied


def public_projects(request):
    """
    Gets all public projects and renders a page with these projects in the context
    Context variables: public_projects
    :param request: The incoming request
    :return: A Render to the public projects page
    """
    public_projects = Project.objects.filter(is_public=True)
    return render(request, 'datacaptureapp/PublicProjects.html/', {'public_projects': public_projects})


def get_node_overview(data, requested_nodes):
    """
    Creates a dictionary with all node keys as keys, and as value another dictionary which has
    all attribute names as keys and the corresponding values as values.
    :param data: The data objects corresponding to the nodes
    :param requested_nodes: The nodes to make an overview for
    :return: The overview
    """
    overview = {}
    for node in requested_nodes:
        overview[node.pk] = {'latitude': node.latitude, 'longitude': node.longitude}
        for data_object in data.filter(node=node):
            overview[node.pk][data_object.attribute.name] = data_object.value
    return overview


@login_required()
def addnode(request, pk):
    """
    If the project exists and the user is allowed to add nodes to this project, renders a page with a form to add a new node.
    If a POST is received, add the node and all of its data to the database and return to the project page
    Context variables: node_form, datas, project_id
    :param request: The incoming request
    :param pk: The id of the project
    :return: A render to the add_node page or a redirect to the project
    """
    requested_project = get_object_or_404(Project, pk=pk)
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
            return render(request, 'datacaptureapp/AddFeature.html',
                          {'node_form': node_form, 'datas': datas, 'project_id': pk})
    else:
        raise PermissionDenied


@login_required()
def nodes(request, pk):
    """
    Renders a page which shows an overview of all nodes and their data of a project, if the user is allowed to.
    If a post request is sent either 2 things can be asked, or a GeoJson/CSV/Excel export of the data, or the removal of a node.
    Context variables: overview, images, attributes
    :param request: The incoming request
    :param pk: The id of the project
    :return: A render to the overview page or a HttpResponse containing a file export.
    """
    requested_project = get_object_or_404(Project, pk=pk)
    if requested_project.is_public or requested_project.user.filter(email=request.user.email).first():
        if request.method == 'POST':
            post = request.POST
            if 'data_type' in post:
                data_type = request.POST.get('data_type')
                if data_type == 'CSV':
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(requested_project.name)
                    generate_csv(response, requested_project)
                elif data_type == 'GeoJSON':
                    geojson = generate_geojson(requested_project)
                    response = HttpResponse(content_type='application/json')
                    response['Content-Disposition'] = 'attachment; filename="{}.geojson"'.format(
                        json.loads(geojson)['name'])
                    response.write(geojson)
                elif data_type == 'Excel':
                    response = HttpResponse(content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(project.name)
                    output = generate_xls(project)
                    response.write(output)
                else:
                    response = HttpResponseServerError('<h1>Something went wrong</h1>')
                return response
            elif 'remove_node' in post:
                Node.objects.get(id=post['remove_node']).delete()
        # No Else statement on purpose, if a node is deleted this code needs to be called.
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
    """

    Context variables:
    :param request: The incoming request
    :param pk: The id of the project
    :param nk: The id of the node
    :return:
    """
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
    """

    Context variables:
    :param request: The incoming request
    :param pk: The id of the project
    :return:
    """
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
    """

    :param request: The incoming request
    :return:
    """
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
    """
    If the user is the owner of the project.
    Context variables:
    :param request: The incoming request
    :return:
    """
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


def login_view(request):
    """
    Renders the login page or logs a user in and redirects to the home page
    Context variables: _
    :param request:
    :return: A Render of the login page or a redirect to the home page
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, 'datacaptureapp/Login.html')


@login_required()
def projects(request):
    """
    Redirects to the home page
    :param request: The incoming request
    :return: A redirect to the home page
    """
    return redirect('home')


@login_required()
def logout_view(request):
    """
    Function that's called when a user logs out, redirects to the login page
    :param request: The incoming request
    :return: A redirect to the login page
    """
    logout(request)
    return redirect("login")


@login_required()
def profile(request):
    """
    Renders the profile page
    Context variables: _
    :param request: The incoming request
    :return: A render of the profile page
    """
    return render(request, 'datacaptureapp/Profile.html')


@login_required()
def newprofile(request):
    """
    Renders the new profile page
    Context variables: _
    :param request: The incoming request
    :return: A render of the NewProfile page
    """
    return render(request, 'datacaptureapp/NewProfile.html')


@login_required()
def editprofile(request):
    """
    Renders the EditProfile page
    Context variables: _
    :param request: The incoming request
    :return: A render of the edit profile page
    """
    return render(request, 'datacaptureapp/EditProfile.html')


def about(request):
    """
    Renders the about page
    Context variables: _
    :param request: The incoming request
    :return: A render of the About page
    """
    return render(request, 'datacaptureapp/About.html')


def faq(request):
    """
    Renders the FAQ page
    Context variables: _
    :param request: The incoming request
    :return: A render of the FAQ page
    """
    return render(request, 'datacaptureapp/FAQ.html')
