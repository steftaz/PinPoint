import csv
import json
from datacaptureapp.models import *


def generate_geojson(project_id):
    project = Project.objects.filter(id=project_id).first()
    nodes = Node.objects.filter(project=project)
    json_node_list = []
    for node in nodes:
        json_node = {"type": "Feature"}
        json_geometry = {"type": "Point", "coordinates": [float(node.longitude), float(node.latitude)]}
        json_node["geometry"] = json_geometry
        datas = Data.objects.filter(node=node)
        json_data = {}
        for data in datas:
            json_data[data.attribute.name] = data.value
        json_node["properties"] = json_data
        json_node_list.append(json_node)
    json_project = {}
    if project is not None:
        json_project["name"] = project.name
    json_project["type"] = "FeatureCollection"
    json_project["features"] = json_node_list
    return json.dumps(json_project)


def generate_csv(response, id):
    project = Project.objects.filter(id=id).first()
    attributes = Attribute.objects.filter(project=project)
    nodes = Node.objects.filter(project=project)
    field_names = ['latitude', 'longitude'] + [attribute.name for attribute in attributes]
    writer = csv.writer(response)
    writer.writerow(field_names)
    for node in nodes:
        writer.writerow([node.latitude, node.longitude] + [data.value for data in Data.objects.filter(node=node)])
