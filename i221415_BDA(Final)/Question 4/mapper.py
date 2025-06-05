#!/usr/bin/env python

import sys
import csv

# Function to calculate engagement by summing retweets and likes
def compute_engagement(retweets, likes):
    try:
        return float(retweets) + float(likes)
    except ValueError:
        return 0.0

# Function to read input from stdin and yield each line
def read_input_lines(file):
    for line in file:
        yield line

# Read input from stdin
input_stream = read_input_lines(sys.stdin)

# Create a CSV reader
reader = csv.reader(input_stream)

# Skip the header row
next(reader)

# Iterate over each row and process the fields
for row in reader:
    # Extract fields from the row
    text = row[1].strip()  
    sentiment = row[2].strip() 
    platform = row[5].strip() 
    retweets = row[7].strip() 
    likes = row[8].strip() 
    country = row[9].strip()  
    
    # Calculate engagement for the current row
    engagement = compute_engagement(retweets, likes)
    
    # Output the processed fields separated by tab
    print(f"{text}\t{platform}\t{country}\t{sentiment}\t{engagement}")
