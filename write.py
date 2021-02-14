"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json
from pathlib import Path
from typing import List, Union

from models import CloseApproach


def float_to_csv(field):
    if field:
        return field
    else:
        return 'nan'


def write_to_csv(results: List[CloseApproach], filename: Union[Path, str]):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    with open(filename, mode='w') as csv_file:
        close_approach_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        close_approach_writer.writerow(fieldnames)
        for result in results:
            close_approach_dict = result.serialize()
            close_approach_neo_dict = result.neo.serialize()
            close_approach_writer.writerow([
                close_approach_dict["datetime_utc"],
                float_to_csv(close_approach_dict["distance_au"]),
                float_to_csv(close_approach_dict["velocity_km_s"]),
                close_approach_neo_dict["designation"],
                close_approach_neo_dict["name"],
                float_to_csv(close_approach_neo_dict["diameter_km"]),
                close_approach_neo_dict["potentially_hazardous"],
            ])


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, mode='w') as json_file:
        counter = 0
        for result in results:
            if counter == 0:
                json_file.write('[')
            else:
                json_file.write(',')
            result_dict = {**result.serialize(), **{"neo": result.neo.serialize()}}
            json.dump(result_dict, json_file)
            json_file.write('\n')
            counter += 1
        json_file.write(']')


