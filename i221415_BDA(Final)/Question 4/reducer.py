#!/usr/bin/env python

import sys
from collections import defaultdict

# Function to read input from file and yield each line as a list of fields
def read_input_rows(file):
    for line in file:
        yield line.strip().split("\t")

# Create a defaultdict to store sentiment counts and engagement
sentiment_counts = defaultdict(lambda: {'positive': 0, 'negative': 0, 'engagement': 0.0})

# Read input from stdin
input_stream = read_input_rows(sys.stdin)

# Iterate over each row and process the fields
for fields in input_stream:
    # Check if the row has the expected number of fields
    if len(fields) != 5:
        continue

    # Extract fields from the row
    text, platform, country, sentiment, engagement = fields

    # Create a key to group by platform and country
    key = f"{platform}-{country}"

    # Update sentiment counts based on the sentiment
    if sentiment.lower() == "positive":
        sentiment_counts[key]['positive'] += 1
    elif sentiment.lower() == "negative":
        sentiment_counts[key]['negative'] += 1
    
    # Update engagement count 
    try:
        sentiment_counts[key]['engagement'] += float(engagement)
    except ValueError:
        # Skip invalid engagement values
        continue

# Print the results
for key, counts in sentiment_counts.items():
    # Output key and counts separated by tab
    print(f"{key}\t{counts['positive']}\t{counts['engagement']}")
