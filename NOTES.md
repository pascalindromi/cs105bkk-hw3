# HW3 notes

Answer each question in a few sentences. Be specific: name the function, the error or the command.

## What did you try?

I implemented everything as required. I also wrote parametrized and focused tests in `test_my_walks.py`. My first instinct was to put `@none_on_error` directly above `parse_walk`, since that is how I would naturally apply a decorator.

## What broke, and how did you fix it?

Curiously, I originally decorated `parse_walk` itself, but soon realizes that it makes invalid rows return `None`, but this function is required to raise `ValueError`. I changed it so `good_walks` applies `none_on_error(parse_walk)` before parsing each row instead; that lets `parse_walk` keep its required behavior while `good_walks` skips bad rows. I used a temporary `.tmp` file for safe writes as specified.

## What would you do differently next time?

i would probably run more tests.
