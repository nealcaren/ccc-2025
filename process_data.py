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
    # Load the tagged left-leaning protests data with Latin encoding
    if Path('ccc-phase3-left-tagged.csv').exists():
        df = pd.read_csv('ccc-phase3-left-tagged.csv', encoding='latin1')
        print(f"Loaded {len(df)} tagged left-leaning events from CSV")
    else:
        df = pd.read_csv('ccc-phase3-left.csv', encoding='latin1')
        print(f"Loaded {len(df)} left-leaning events from CSV (untagged)")

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
    
    # Calculate total size, using 11 as default where size is unknown
    df['size_for_total'] = df['size_mean'].fillna(11)
    total_size = int(df['size_for_total'].sum())
    
    summary_stats = {
        'total_events': len(df),
        'unique_locations': df['locality'].nunique(),
        'total_size': total_size,
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
    
    # 5b. Generate state size averages
    # Fill missing size values with 11
    df['size_for_avg'] = df['size_mean'].fillna(11)
    # Group by state and calculate average size
    state_size_data = df.groupby('state')['size_for_avg'].mean().to_dict()
    with open('data/states_size.json', 'w') as f:
        json.dump(state_size_data, f)
    
    # 6. Generate tactics breakdown (old)
    if 'participant_measures' in df.columns:
        tactics_data = df['participant_measures'].value_counts().head(20).to_dict()
        with open('data/tactics.json', 'w') as f:
            json.dump(tactics_data, f)
        print(f"Saved top {len(tactics_data)} tactics")
    
    # 7. Generate new tactics analysis
    print("Generating tactics analysis...")
    
    # Initialize tactics columns
    df['tactic_demonstration'] = 0
    df['tactic_march'] = 0
    df['tactic_counter_protest'] = 0
    df['tactic_civil_disobedience'] = 0
    df['tactic_arrests'] = 0
    df['tactic_vigil'] = 0
    
    # Demonstration: includes demonstration, rally, protest
    demonstration_terms = ['demonstration', 'rally', 'protest']
    df['tactic_demonstration'] = df['event_type'].fillna('').apply(
        lambda x: 1 if any(term in x.lower() for term in demonstration_terms) else 0
    )
    
    # March
    df['tactic_march'] = df['event_type'].fillna('').apply(
        lambda x: 1 if 'march' in x.lower() else 0
    )
    
    # Counter-protest
    df['tactic_counter_protest'] = df['event_type'].fillna('').apply(
        lambda x: 1 if 'counter' in x.lower() else 0
    )
    
    # Civil disobedience
    df['tactic_civil_disobedience'] = df['event_type'].fillna('').apply(
        lambda x: 1 if 'civil disobedience' in x.lower() or 'disobedience' in x.lower() else 0
    )
    
    # Arrests (from arrests_any)
    df['tactic_arrests'] = df['arrests_any']
    
    # Vigil (from participant_measures)
    df['tactic_vigil'] = df['participant_measures'].fillna('').apply(
        lambda x: 1 if 'vigil' in x.lower() else 0
    )
    
    # Calculate percentages
    total_events = len(df)
    tactics_percentages = {
        'March': (df['tactic_march'].sum() / total_events) * 100,
        'Counter-Protest': (df['tactic_counter_protest'].sum() / total_events) * 100,
        'Civil Disobedience': (df['tactic_civil_disobedience'].sum() / total_events) * 100,
        'Arrests': (df['tactic_arrests'].sum() / total_events) * 100,
        'Vigil': (df['tactic_vigil'].sum() / total_events) * 100
    }
    
    # Save tactics data to JSON for the dashboard
    tactics_json = {
        'labels': list(tactics_percentages.keys()),
        'percentages': list(tactics_percentages.values()),
        'counts': [
            int(df['tactic_march'].sum()),
            int(df['tactic_counter_protest'].sum()),
            int(df['tactic_civil_disobedience'].sum()),
            int(df['tactic_arrests'].sum()),
            int(df['tactic_vigil'].sum())
        ]
    }
    
    with open('data/tactics_analysis.json', 'w') as f:
        json.dump(tactics_json, f)
    
    print(f"Saved tactics analysis")

    print("Data processing complete. JSON files generated in the 'data' directory.")

if __name__ == "__main__":
    main()
