from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/public/', views.public_projects, name='public-projects'),
    path('projects/<int:pk>/', views.project, name='project'),
    path('projects/new/', views.newproject, name='new-project'),
    path('projects/<int:pk>/attributes/', views.add_attribute, name='attributes'),
    path('projects/<int:pk>/nodes/new/', views.addnode, name='addnode'),
    path('projects/<int:pk>/nodes/', views.nodes, name='nodes'),
    path('projects/<int:pk>/nodes/<int:nk>/edit/', views.edit_node, name='edit-node'),
    path('projects/<int:pk>/team/', views.team, name='team'),
    # path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/new', views.newprofile, name='new-profile'),
    path('profile/edit', views.editprofile, name='edit-profile'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('FAQ/', views.faq, name='faq'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]

