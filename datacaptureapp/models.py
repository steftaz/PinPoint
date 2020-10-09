from django.db import models
from account.models import Account


# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=50)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)  # A project belongs to a single user


class Form(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)  # A form belongs to a single project


class Attribute(models.Model):
	form = models.ForeignKey(Form, on_delete=models.CASCADE)  # An attribute belongs to a single form
	type = models.CharField(max_length=50)
	value = models.CharField(max_length=50)
