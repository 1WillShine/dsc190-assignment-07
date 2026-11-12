import marimo

app = marimo.App()


@app.cell
def _():
    import csv
    from pathlib import Path

    import matplotlib.pyplot as plt
    return Path, csv, plt


@app.cell
def _(Path, csv):
    events_path = Path(__file__).resolve().parents[1] / "data" / "features" / "events.csv"
    with events_path.open(newline="", encoding="utf-8") as events_file:
        durations = [float(row["duration_minutes"]) for row in csv.DictReader(events_file)]
    return (durations,)


@app.cell
def _(durations, plt):
    figure, axes = plt.subplots()
    axes.hist(durations, bins=20)
    axes.set(xlabel="Duration (minutes)", ylabel="Events", title="Event durations")
    figure
    return


if __name__ == "__main__":
    app.run()
