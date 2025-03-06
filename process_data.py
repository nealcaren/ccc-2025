import pandas as pd
import json
import os
from pathlib import Path

def main():
    # Create directories for output
    Path('data').mkdir(exist_ok=True)
    Path('public').mkdir(exist_ok=True)

    print("Loading dataset details...")
    # Load the dataset details for reference
    with open('ccc-phase3-public_details.json', 'r') as f:
        dataset_details = json.load(f)

    print("Loading CSV data...")
    # Load the actual CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # 1. Generate events by day count
    print("Generating events by day count...")
    date_counts = df['date'].value_counts().sort_index().to_dict()

    # Save date counts to JSON for the chart
    with open('data/date_counts.json', 'w') as f:
        json.dump(date_counts, f)
    print(f"Saved date counts for {len(date_counts)} days")

    # 2. Create a table of events with key fields
    print("Creating events table...")
    # Select important columns
    key_columns = ['date', 'locality', 'state', 'event_type', 'size_mean', 'targets', 'claims_summary']
    # Include all events, not just the first 100
    events_table = df[key_columns].fillna('Unknown').to_dict(orient='records')

    # Save events table to JSON
    with open('data/events_table.json', 'w') as f:
        json.dump(events_table, f)
    print(f"Saved details for {len(events_table)} events")

    # 3. Generate summary statistics
    print("Generating summary statistics...")
    summary_stats = {
        'total_events': len(df),
        'unique_locations': df['locality'].nunique(),
        'unique_states': df['state'].nunique(),
        'event_types': df['event_type'].value_counts().head(5).to_dict(),
        'top_targets': df['targets'].value_counts().head(5).to_dict() if 'targets' in df.columns else {},
        'top_claims': {k[:50] + '...' if len(k) > 50 else k: v 
                      for k, v in df['claims_summary'].value_counts().head(5).to_dict().items()},
    }

    # Save summary stats to JSON
    with open('data/summary_stats.json', 'w') as f:
        json.dump(summary_stats, f)
    
    # 4. Generate event types breakdown
    event_types_data = df['event_type'].value_counts().to_dict()
    with open('data/event_types.json', 'w') as f:
        json.dump(event_types_data, f)
    
    # 5. Generate state breakdown
    state_data = df['state'].value_counts().to_dict()
    with open('data/states.json', 'w') as f:
        json.dump(state_data, f)
    
    # 6. Generate tactics breakdown
    if 'participant_measures' in df.columns:
        tactics_data = df['participant_measures'].value_counts().head(20).to_dict()
        with open('data/tactics.json', 'w') as f:
            json.dump(tactics_data, f)
        print(f"Saved top {len(tactics_data)} tactics")

    print("Data processing complete. JSON files generated in the 'data' directory.")

if __name__ == "__main__":
    main()
