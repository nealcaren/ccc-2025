import pandas as pd
from pathlib import Path

def main():
    print("Loading CSV data...")
    # Load the CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # Create tactics columns
    print("Analyzing tactics...")
    
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
        'Demonstration': (df['tactic_demonstration'].sum() / total_events) * 100,
        'March': (df['tactic_march'].sum() / total_events) * 100,
        'Counter-Protest': (df['tactic_counter_protest'].sum() / total_events) * 100,
        'Civil Disobedience': (df['tactic_civil_disobedience'].sum() / total_events) * 100,
        'Arrests': (df['tactic_arrests'].sum() / total_events) * 100,
        'Vigil': (df['tactic_vigil'].sum() / total_events) * 100
    }
    
    # Save tactics data to CSV
    tactics_df = pd.DataFrame({
        'tactic': list(tactics_percentages.keys()),
        'percentage': list(tactics_percentages.values()),
        'count': [
            df['tactic_demonstration'].sum(),
            df['tactic_march'].sum(),
            df['tactic_counter_protest'].sum(),
            df['tactic_civil_disobedience'].sum(),
            df['tactic_arrests'].sum(),
            df['tactic_vigil'].sum()
        ]
    })
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    output_file = 'data/tactics_analysis.csv'
    tactics_df.to_csv(output_file, index=False)
    print(f"Saved tactics analysis to {output_file}")
    
    # Save to JSON for the dashboard
    tactics_json = {
        'labels': list(tactics_percentages.keys()),
        'percentages': list(tactics_percentages.values()),
        'counts': [
            int(df['tactic_demonstration'].sum()),
            int(df['tactic_march'].sum()),
            int(df['tactic_counter_protest'].sum()),
            int(df['tactic_civil_disobedience'].sum()),
            int(df['tactic_arrests'].sum()),
            int(df['tactic_vigil'].sum())
        ]
    }
    
    import json
    with open('data/tactics_analysis.json', 'w') as f:
        json.dump(tactics_json, f)
    
    # Print results
    print("\nTactics Analysis:")
    for tactic, percentage in tactics_percentages.items():
        count = df[f"tactic_{tactic.lower().replace('-', '_').replace(' ', '_')}"].sum()
        print(f"{tactic}: {percentage:.2f}% ({count} events)")

if __name__ == "__main__":
    main()
