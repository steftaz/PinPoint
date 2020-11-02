from django.db import models
from account.models import Account


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(Account)
    is_public = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Attribute(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # A form belongs to a single project
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()


class Node(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=11)
    picture = models.ImageField(upload_to='images', blank=True)
    date_time_stored = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Account, blank=True, null=True, on_delete=models.SET_NULL)


class Data(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)