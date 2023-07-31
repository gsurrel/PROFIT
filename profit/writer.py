import csv


def to_csv(data, path):
    """Write the provided data (as a list of dicts) to a CSV file under the specified folder"""

    with open(path, "w", newline="") as csvfile:
        fieldnames = data[0].keys() if len(data) else [""]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for sample in data:
            writer.writerow(sample)

    print(f"Written collected data to {path}")
