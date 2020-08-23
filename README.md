# Find-Matching-Phrases

A wrapper with interactive CLI that allows you to categorize a CSV of unstructured text data with another CSV of substrings/phrases



### Setup

It works out of the box with Python3

### Usage

You'll need:
* a CSV of text
* a CSV of substrings/phrases (and optionally, categories of those substrings/phrases)

Start the execution with
```py
python3 match_csv_phrases.py
```

The script will iterate over each row in the text CSV and write to a new CSV. Backup writes to the output CSV are provided every 1000 rows, as well.
