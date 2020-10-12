from django.db import models
from account.models import Account


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ManyToManyField(Account)  # A project belongs to a single user

    # def get_name(self):
    #     return self.name
    #
    # def get_description(self):
    #     return self.description
    #
    # def get_user(self):
    #     return self.user


class Attribute(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # A form belongs to a single project
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()

    # def get_project(self):
    #     return self.project
    #
    # def get_type(self):
    #     return self.type
    #
    # def get_name(self):
    #     return self.name
    #
    # def get_description(self):
    #     return self.description


class Node(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=11)

    # def get_project(self):
    #     return self.project
    #
    # def get_latitude(self):
    #     return self.latitude
    #
    # def get_longitude(self):
    #     return self.longitude


class Data(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    # def get_attribute(self):
    #     return self.attribute
    #
    # def get_node(self):
    #     return self.node
    #
    # def get_value(self):
    #     return self.value

