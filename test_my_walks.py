"""Part 10: your own tests for parse_walk. The README says what to write here.

We grade this file by running it against a correct walks.py, where every test must pass,
and against versions of walks.py with a bug planted in parse_walk, where your tests should fail.
"""

import pytest

from walks import Walk, parse_walk


@pytest.fixture
def good_row() -> dict[str, str]:
    """Provided: one good row, as csv.DictReader gives it. Each test gets its own new copy."""
    return {"date": "2026-11-16", "steps": "4200", "place": "Lumphini Park"}


def test_core_example_a_good_row_becomes_a_walk(good_row):
    """Provided: an example that uses the fixture. Write your own tests below it."""
    assert parse_walk(good_row) == Walk("2026-11-16", 4200, "Lumphini Park")


# Your tests go here.
def test_cleaned_fields_keep_whole_number_and_strip_spaces(good_row):
    good_row.update({"date": " 2026-11-18 ", "steps": " 0 ", "place": " campus "})
    assert parse_walk(good_row) == Walk("2026-11-18", 0, "campus")


@pytest.mark.parametrize(
    "field,value",
    [
        ("date", ""),
        ("date", "   "),
        ("steps", ""),
        ("steps", "abc"),
        ("steps", "12.5"),
        ("steps", "-300"),
    ],
)
def test_bad_required_values_raise_value_error(good_row, field, value):
    good_row[field] = value
    with pytest.raises(ValueError):
        parse_walk(good_row)


def test_missing_date_key_is_rejected(good_row):
    del good_row["date"]
    with pytest.raises(ValueError):
        parse_walk(good_row)


def test_missing_steps_key_is_rejected(good_row):
    del good_row["steps"]
    with pytest.raises(ValueError):
        parse_walk(good_row)


def test_zero_steps_is_allowed(good_row):
    good_row["steps"] = "0"
    assert parse_walk(good_row).steps == 0
