import pandas as pd
from pathlib import Path

def main():
    print("Loading CSV data...")
    # Load the CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # Extract tactics and count frequencies
    print("Analyzing tactics (participant_measures)...")
    tactics_series = df['participant_measures'].fillna('Unknown')
    
    # Count frequencies
    tactics_counts = tactics_series.value_counts().reset_index()
    tactics_counts.columns = ['tactic', 'count']
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    output_file = 'data/tactics_counts.csv'
    tactics_counts.to_csv(output_file, index=False)
    print(f"Saved {len(tactics_counts)} unique tactics to {output_file}")
    
    # Print top 10 tactics
    print("\nTop 10 tactics:")
    for i, (tactic, count) in enumerate(zip(tactics_counts['tactic'][:10], tactics_counts['count'][:10])):
        print(f"{i+1}. {tactic}: {count}")

if __name__ == "__main__":
    main()
