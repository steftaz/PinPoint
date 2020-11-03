import io
import json
import zipfile
from xlsxwriter import Workbook
from datacaptureapp.models import *
import gisproject.settings as settings


def generate_geojson(project):
    """
    Generates a zip containing a csv representation of the given project and all of it's pictures.
    Geojson file is featurecollection with point features, which properties contain the data of a point and the URL to the picture.
    Empty values are shown as Null.
    :param project: The project for which the Geojson export needs to be made
    :return: String containing the geojson dump
    """
    mem_file = io.BytesIO()
    with zipfile.ZipFile(mem_file, "w") as zip_file:
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
            json_data['picture'] = node.picture.name if node.picture else 'Null'
            json_node["properties"] = json_data
            json_node_list.append(json_node)
            if node.picture:
                zip_file.write(settings.MEDIA_URL[1:] + node.picture.name, node.picture.name)
        json_project = {}
        if project is not None:
            json_project["name"] = project.name
        json_project["type"] = "FeatureCollection"
        json_project["features"] = json_node_list
        json_string = json.dumps(json_project)

        zip_file.writestr("{}.geojson".format(project.name), json_string)
    return mem_file.getvalue()


def generate_csv(project):
    """
    Generates a zip containing a csv representation of the given project and all of it's pictures.
    CSV columns contain the latitude, longitude, all attributes of a node and the URL to the picture.
    1 row represents 1 node.
    Empty values are shown as Null.
    :param project: The project for which the csv export needs to be made
    :return: The zip file in a BytesIO
    """
    mem_file = io.BytesIO()
    with zipfile.ZipFile(mem_file, "w") as zip_file:
        attributes = Attribute.objects.filter(project=project)
        nodes = Node.objects.filter(project=project)
        field_names = ['latitude', 'longitude'] + [attribute.name for attribute in attributes] + ['picture']
        csv = write_csv_row('', field_names)
        for node in nodes:
            row = [node.latitude, node.longitude] + [data.value for data in Data.objects.filter(node=node)]
            if node.picture:
                zip_file.write(settings.MEDIA_URL[1:] + node.picture.name, node.picture.name)
                row.append(node.picture.name)
            else:
                row.append('Null')
            csv = write_csv_row(csv, row)
        zip_file.writestr("{}.csv".format(project.name), csv)
    return mem_file.getvalue()


def write_csv_row(csv, row):
    """
    Writes a row in csv format to the given string
    :param csv: The old csv string
    :param row: List containing the elements to be written in the new row
    :return: The new csv string including the row, appended with \n
    """
    for val in row:
        csv += '{},'.format(val)
    return csv + '\n'


def generate_xlsx(project):
    """
    Generates a zip containing an excel representation of the given project and all of it's pictures.
    CSV columns contain the latitude, longitude, all attributes of a node and the URL to the picture.
    1 row represents 1 node.
    Empty values are shown as Null.
    :param project: The project for which the excel export needs to be made
    :return: The zip file in a BytesIO
    """
    mem_file = io.BytesIO()
    with zipfile.ZipFile(mem_file, "w") as zip_file:
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
            if node.picture:
                zip_file.write(settings.MEDIA_URL[1:] + node.picture.name, node.picture.name)
                worksheet.write(row, col, node.picture.name)
            else:
                worksheet.write(row, col, "Null")
        workbook.close()
        zip_file.writestr("{}.xlsx".format(project.name), output.getvalue())
    return mem_file.getvalue()
