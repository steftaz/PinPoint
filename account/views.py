from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm, AccountAuthenticationForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            print('successful account creation')
            return redirect('projects')
        else:
            # add errors to context (form is not valid)
            context['registration_form'] = form
    else:
        # GET request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)


def login_view(request):
    print("login")
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("projects")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("projects")
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(redirect, 'account/login.html', context)
