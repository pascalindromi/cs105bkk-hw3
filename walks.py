"""HW3 · walks.py: read the step counter's CSV file and keep only the good rows. Practises
Session 7 (reading a CSV file, cleaning data) and Session 9 (a generator and a decorator)."""

import csv
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from functools import wraps
from pathlib import Path


@dataclass
class Walk:
    """Provided: one walk from the log, cleaned. `steps` is a whole number, 0 or more."""

    date: str
    steps: int
    place: str

def parse_walk(row: dict[str, str]) -> Walk:
    """Turn one row of the CSV file into a Walk, or raise ValueError if the row is bad."""
    date = row.get("date", "").strip()
    if not date:
        raise ValueError("date is empty")

    text_steps = row.get("steps", "").strip()
    try:
        steps = int(text_steps)
    except ValueError:
        raise ValueError(f"steps is not a whole number: {text_steps}")

    if steps < 0:
        raise ValueError(f"steps is below 0: {steps}")

    place = row.get("place", "").strip()
    return Walk(date, steps, place)


def none_on_error(func: Callable) -> Callable:
    """A decorator: the wrapped function returns None instead of raising ValueError."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None

    return wrapper


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    """Yield the rows of a CSV file one at a time, each as a dict of text."""
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def good_walks(rows: Iterable[dict[str, str]]) -> Iterator[Walk]:
    """Yield a Walk for every good row, one at a time, and skip the bad ones."""
    parse_if_valid = none_on_error(parse_walk)
    for row in rows:
        walk = parse_if_valid(row)
        if walk is not None:
            yield walk