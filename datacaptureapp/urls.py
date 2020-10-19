from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.projects, name='projects'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project, name='project'),
    path('projects/new/', views.newproject, name='new-project'),
    path('projects/<int:pk>/attributes/', views.add_attribute, name='attributes'),
    # path('projects/<int:pk>/attributes/new/', views.add_attribute, name='new-attribute'),
    path('projects/<int:pk>/nodes/new/', views.addnode, name='addnode'),
    path('projects/<int:pk>/nodes/', views.nodes, name='nodes'),
    # path('login/', views.login),
    path('profile/', views.profile),
    path('newprofile/', views.newprofile),
    path('logout/', views.logout_view)
]
