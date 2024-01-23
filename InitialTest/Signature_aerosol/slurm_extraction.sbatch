#!/bin/bash

# SLURM directives
#SBATCH --partition=short-serial
#SBATCH --job-name=caliop_extraction_$1
#SBATCH --time=24:00:00
#SBATCH --mem=16000

# Calculate start and end dates based on the month passed as a parameter
month=$1
start_date="2017-${month}-01"
end_date=$(date -d "$start_date + 1 month - 1 day" +%Y-%m-%d)

# Loop over each day
current_sec=start_date
while [ $current_sec -le $end_sec ]; do
    # Convert the current date in seconds back to a readable format
    current_date=$(date -d @$current_sec +%Y-%m-%d)

    # Run the python command with the current date
    python caliop_extraction.py $current_date

    # Move to the next day (86400 seconds in a day)
    current_sec=$((current_sec+86400))
done
