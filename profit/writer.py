import csv
import os

from shutil import copyfile


def to_csv(data, path):
    """Write the provided data (as a list of dicts) to a CSV file under the specified folder"""

    # Filter out the empty values we may get
    data = list(filter(lambda i: i != None, data))

    # Generate a field with a stable pid column
    data = list(
        map(lambda d: {"pid_stable": f"{d['pid']} {d['creation_epoch']}", **d}, data)
    )

    # Write data
    with open(path, "w", newline="") as csvfile:
        fieldnames = data[0].keys() if len(data) else [""]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for sample in data:
            writer.writerow(sample)

    print(f"Written collected data to {path}")


def generate_visualization(path):
    """Copy the required files to get the visualization working"""
    viz_root = os.path.dirname(os.path.realpath(__name__)) + "/profit/viz/"

    # List files to copy
    files = [
        os.path.join(dirpath, f)
        for (dirpath, dirnames, filenames) in os.walk(viz_root)
        for f in filenames
    ]

    # Copy files
    for filename in files:
        copyfile(
            os.path.dirname(os.path.realpath(__name__)) + "/profit/viz/" + filename,
            path / filename,
        )
