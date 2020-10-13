from django.shortcuts import render

def home(request):
  return render(request, 'datacaptureapp/home.html', {})

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
