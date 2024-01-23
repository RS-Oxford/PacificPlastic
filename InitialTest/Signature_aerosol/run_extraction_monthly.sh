#!/bin/bash

# Start date
start_date="2017-01-01"

# End date
end_date="2017-01-31"

# Convert the start and end dates to seconds since the epoch
start_sec=$(date -d "$start_date" +%s)
end_sec=$(date -d "$end_date" +%s)

# Loop over each day
current_sec=$start_sec
while [ $current_sec -le $end_sec ]; do
    # Convert the current date in seconds back to a readable format
    current_date=$(date -d @$current_sec +%Y-%m-%d)

    # Run the python command with the current date
    python caliop_extraction.py $current_date

    # Move to the next day (86400 seconds in a day)
    current_sec=$((current_sec+86400))
done