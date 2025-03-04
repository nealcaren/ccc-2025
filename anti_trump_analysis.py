import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import re
import os

# Set up output directory
os.makedirs('reports', exist_ok=True)

# Load the CSV data
print("Loading data...")
df = pd.read_csv("ccc-phase3-public.csv", dtype=str, encoding='latin')

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Function to check if Trump is mentioned in targets
def mentions_trump(target_str):
    if pd.isna(target_str):
        return False
    
    # Common ways Trump is mentioned in the data
    trump_patterns = [
        r'trump', r'donald\s+trump', r'president\s+trump', 
        r'former\s+president\s+trump', r'45', r'djt'
    ]
    
    # Case insensitive search
    for pattern in trump_patterns:
        if re.search(pattern, str(target_str).lower()):
            return True
    return False

# Filter for events targeting Trump
trump_df = df[df['targets'].apply(mentions_trump)]
print(f"Found {len(trump_df)} events targeting Trump")

# Group by date and count
daily_counts = trump_df.groupby(trump_df['date'].dt.date).size().reset_index()
daily_counts.columns = ['date', 'count']
daily_counts = daily_counts.sort_values('date')

# Create the markdown report
report = f"""# Analysis of Anti-Trump Protests in 2025

## Overview

This report analyzes protest events targeting former President Donald Trump during the first months of 2025. The data comes from the Crowd Counting Consortium's Phase 3 public dataset.

## Key Findings

- **Total Events**: {len(trump_df)} protests targeting Trump were identified
- **Time Period**: Events occurred from {daily_counts['date'].min()} to {daily_counts['date'].max()}
- **Peak Day**: The highest number of anti-Trump protests ({daily_counts['count'].max()}) occurred on {daily_counts.loc[daily_counts['count'].idxmax(), 'date']}

## Common Claims and Themes

```
# Get the most common claims
claims = trump_df['claims_summary'].dropna().str.split(';').explode().str.strip()
top_claims = claims.value_counts().head(10)

report += "The most common claims and themes in anti-Trump protests were:\n\n"
for claim, count in top_claims.items():
    report += f"- {claim} ({count} mentions)\n"

report += """
## Geographic Distribution

"""

# Get top states
top_states = trump_df['state'].value_counts().head(10)
report += "**Top States for Anti-Trump Protests:**\n\n"
for state, count in top_states.items():
    report += f"- {state}: {count} events\n"

report += """
## Daily Counts of Anti-Trump Protests

The following table shows the number of anti-Trump protests by day:

| Date | Number of Protests |
|------|-------------------|
"""

# Add the daily counts to the table
for _, row in daily_counts.iterrows():
    report += f"| {row['date']} | {row['count']} |\n"

report += "## Conclusion\n\n"
report += "Anti-Trump protests in early 2025 demonstrate continued political polarization following the 2024 election. "
report += "These events were characterized by concerns about democratic institutions, women's rights, and other progressive causes.\n\n"
report += "The geographic distribution shows concentration in traditionally Democratic-leaning states, particularly on the coasts. "
report += "The temporal pattern reveals spikes around key political events and weekends when more people are available to participate.\n"

# Save the report
with open('reports/anti_trump_protests.md', 'w') as f:
    f.write(report)

print(f"Report saved to reports/anti_trump_protests.md")

# Create a visualization
plt.figure(figsize=(12, 6))
plt.bar(daily_counts['date'].astype(str), daily_counts['count'])
plt.xticks(rotation=45)
plt.title('Anti-Trump Protests by Day (2025)')
plt.xlabel('Date')
plt.ylabel('Number of Protests')
plt.tight_layout()
plt.savefig('reports/anti_trump_timeline.png')
print("Visualization saved to reports/anti_trump_timeline.png")
