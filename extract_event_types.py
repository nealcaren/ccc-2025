import pandas as pd
from pathlib import Path

def main():
    print("Loading CSV data...")
    # Load the CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # Extract event types and count frequencies
    print("Analyzing event types...")
    event_types_series = df['event_type'].fillna('Unknown')
    
    # Count frequencies
    event_types_counts = event_types_series.value_counts().reset_index()
    event_types_counts.columns = ['event_type', 'count']
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    output_file = 'data/event_types_counts.csv'
    event_types_counts.to_csv(output_file, index=False)
    print(f"Saved {len(event_types_counts)} unique event types to {output_file}")
    
    # Print all event types
    print("\nAll event types:")
    for i, (event_type, count) in enumerate(zip(event_types_counts['event_type'], event_types_counts['count'])):
        print(f"{i+1}. {event_type}: {count}")

if __name__ == "__main__":
    main()
