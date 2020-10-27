import csv
import io
import json
from PIL import Image
from xlsxwriter import Workbook
from datacaptureapp.models import *


def generate_geojson(project):
    """
    Generates a geojson representation of the given project.
    Geojson file is featurecollection with point features, which properties contain the data of a point.
    :param project: The project for which the Geojson export needs to be made
    :return: String containing the geojson dump
    """
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


def generate_csv(response, project):
    """
    Generates a csv representation of the given project.
    Columns contain the latitude, longitude and all attributes of a node.
    1 row represents 1 node
    :param response: The httpresponse to which the csv content needs to be added
    :param project: The project for which the csv export needs to be made
    :return: None
    """
    attributes = Attribute.objects.filter(project=project)
    nodes = Node.objects.filter(project=project)
    field_names = ['latitude', 'longitude'] + [attribute.name for attribute in attributes]
    writer = csv.writer(response)
    writer.writerow(field_names)
    for node in nodes:
        writer.writerow([node.latitude, node.longitude] + [data.value for data in Data.objects.filter(node=node)])
    return


def generate_xls(project):
    """
    Generates an excel representation of the given project.
    Columns contain the latitude, longitude, all attributes and the picture of a node.
    1 row represents 1 node
    If the node contains a picture, it will include a scaled down version of the picture which can be scaled up to the original size
    :param project: The project for which the excel export needs to be made
    :return: The entire content of the excel file
    """
    attributes = Attribute.objects.filter(project=project)
    nodes = Node.objects.filter(project=project)
    output = io.BytesIO()
    workbook = Workbook(output)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for x in ['latitude', 'longitude'] + [attribute.name for attribute in attributes] + ['picture']:
        worksheet.write(row, col, x)
        col += 1
    for node in nodes:
        row += 1
        col = 0
        for x in [node.latitude, node.longitude] + [data.value.format() for data in Data.objects.filter(node=node)]:
            worksheet.write(row, col, x)
            col += 1
        if node.picture.name != "":
            path = "media/{}".format(node.picture.name)
            width, height = Image.open(path).size
            scale = 64 / width
            worksheet.insert_image(row, col, path, {'x_scale': scale, 'y_scale': scale})
            worksheet.set_row(row, height * scale)
        else:
            worksheet.write(row, col, "Null")
    workbook.close()
    return output.getvalue()
