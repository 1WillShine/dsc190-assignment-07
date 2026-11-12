import csv
from datetime import date, datetime
from pathlib import Path
import sys

EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def clean(row):
    if any(value is None or not value.strip() for value in row.values()):
        return None
    if row["event_type"] not in EVENT_TYPES:
        return None
    duration = int(row["duration_seconds"])
    if duration <= 0:
        return None
    timestamp = row["timestamp"]
    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError:
        parsed = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
    return {**row, "timestamp": parsed.isoformat(timespec="seconds"), "duration_seconds": duration}


def transform(row):
    return {**row, "date": row["timestamp"].split("T")[0]}


def features(row):
    return {
        **row,
        "duration_minutes": int(row["duration_seconds"]) / 60,
        "weekday": WEEKDAYS[date.fromisoformat(row["date"]).weekday()],
    }


def main(stage, source, destination):
    process, extra_columns = {
        "clean": (clean, []),
        "transform": (transform, ["date"]),
        "features": (features, ["duration_minutes", "weekday"]),
    }[stage]
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(source, newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        with destination.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=[*reader.fieldnames, *extra_columns])
            writer.writeheader()
            for row in reader:
                result = process(row)
                if result is not None:
                    writer.writerow(result)


if __name__ == "__main__":
    main(*sys.argv[1:])
