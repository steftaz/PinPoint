from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # password reset
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
         name='password_change_done'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'),
         name='password_change'),
]
