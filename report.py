"""HW3 · report.py: add up the steps and save a report as JSON. Practises Session 7 (writing
and reading JSON) and Session 9 (a context manager)."""

import json
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from walks import Walk, good_walks, read_rows


def steps_per_day(walks: Iterable[Walk]) -> dict[str, int]:
    """Total steps for each date, with the dates in order, earliest first."""
    totals = {}

    for walk in walks:
        totals[walk.date] = totals.get(walk.date, 0) + walk.steps

    return dict(sorted(totals.items()))

def best_day(totals: dict[str, int]) -> str:
    """The date with the most steps. On a tie, the earliest of those dates."""
    if not totals:
        raise ValueError("there are no days")
    highest = max(totals.values())

    best_date = None

    for date, steps in totals.items():
        if steps == highest:
            if best_date is None or date < best_date:
                best_date = date

    return best_date

@contextmanager
def saved_safely(path: Path) -> Iterator[TextIO]:
    """Write to a new file, and put it in place of `path` only if the with block ends without an error."""
    tempfile = path.with_name(path.name + ".tmp")
    try:
        with tempfile.open("w", encoding="utf-8") as file:
            yield file
        tempfile.replace(path)
    except BaseException:
        tempfile.unlink(missing_ok=True)
        raise


def write_report(path: Path, walks: Iterable[Walk]) -> dict:
    """Save the week's report to a JSON file, and return it as a dict."""
    days = steps_per_day(walks)
    report = {
        "total_steps": sum(days.values()),
        "best_day": best_day(days),
        "days": days,
    }
    with saved_safely(path) as file:
        json.dump(report, file, indent=2)
    return report


def load_report(path: Path) -> dict | None:
    """The report saved last time, or None if there is no file or it is not valid JSON."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


if __name__ == "__main__":
    # Provided: runs only with `python report.py`, not on import.
    here = Path(__file__).parent
    last_time = load_report(here / "report.json")
    report = write_report(here / "report.json", good_walks(read_rows(here / "walks.csv")))
    print(f"{report['total_steps']} steps this week. Best day: {report['best_day']}.")
    if last_time is not None:
        print(f"Last time you saved {last_time['total_steps']} steps.")
