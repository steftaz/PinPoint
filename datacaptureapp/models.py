from django.db import models
from account.models import Account


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ManyToManyField(Account)  # A project belongs to a single user


class Attribute(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # A form belongs to a single project
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()


class Node(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=11)


class Data(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
