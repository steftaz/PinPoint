import os
import django
import json
from manage import DEFAULT_SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
django.setup()
from datacaptureapp.models import *

def generate_geojson(project_id):
    project = Project.objects.filter(id=project_id).first()
    nodes = Node.objects.filter(project=project)
    JSNodeList = []
    for node in nodes:
        JSNode = {}
        JSNode["type"] = "Feature"
        JSGeometry = {}
        JSGeometry["type"] = "Point"
        JSGeometry["coordinates"] = [float(node.latitude), float(node.longitude)]
        JSNode["geometry"] = JSGeometry
        datas = Data.objects.filter(node=node)
        JSData = {}
        for data in datas:
            JSData[data.attribute.name] = data.value
        JSNode["properties"] = JSData
        JSNodeList.append(JSNode)
    JSProject = {}
    if project is not None:
        JSProject["name"] = project.name
    JSProject["type"] = "FeatureCollection"
    JSProject["features"] = JSNodeList
    return json.dumps(JSProject)


# print(generate_geojson(1))
