import pandas as pd
import json
import os

# Create directories for output
os.makedirs('data', exist_ok=True)
os.makedirs('public', exist_ok=True)

# Load the dataset details for reference
with open('ccc-phase3-public_details.json', 'r') as f:
    dataset_details = json.load(f)

# Load the actual CSV data
# Note: You'll need to update the path if your CSV is in a different location
df = pd.read_csv('ccc-phase3-public.csv')

# 1. Generate events by day count
date_counts = df['date'].value_counts().sort_index().to_dict()

# Save date counts to JSON for the chart
with open('data/date_counts.json', 'w') as f:
    json.dump(date_counts, f)

# 2. Create a table of events with key fields
# Select important columns
key_columns = ['date', 'locality', 'state', 'event_type', 'size_mean', 'targets', 'claims_summary']
events_table = df[key_columns].fillna('Unknown').head(100).to_dict(orient='records')

# Save events table to JSON
with open('data/events_table.json', 'w') as f:
    json.dump(events_table, f)

# 3. Generate summary statistics
summary_stats = {
    'total_events': len(df),
    'unique_locations': df['locality'].nunique(),
    'unique_states': df['state'].nunique(),
    'event_types': df['event_type'].value_counts().head(5).to_dict(),
    'top_targets': df['targets'].value_counts().head(5).to_dict() if 'targets' in df.columns else {},
}

# Save summary stats to JSON
with open('data/summary_stats.json', 'w') as f:
    json.dump(summary_stats, f)

print("Data processing complete. JSON files generated in the 'data' directory.")
