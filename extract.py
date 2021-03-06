"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    hazardous_map = {"Y": True, "N": False}
    with open(neo_csv_path) as infile:
        reader = csv.reader(infile)
        header = next(reader)
        for row in reader:
            neos.append(
                NearEarthObject(
                    designation=row[header.index("pdes")],
                    name=row[header.index("name")],
                    diameter=row[header.index("diameter")],
                    hazardous=hazardous_map.get(row[header.index("pha")], None),
                )
            )
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path) as f:
        close_approaches = []
        ca_dict = json.load(f)
        header = ca_dict["fields"]
        for row in ca_dict["data"]:
            close_approaches.append(
                CloseApproach(
                    designation=row[header.index("des")],
                    time=row[header.index("cd")],
                    distance=row[header.index("dist")],
                    velocity=row[header.index("v_rel")],
                )
            )
    return close_approaches
