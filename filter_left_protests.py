import pandas as pd
from pathlib import Path

def main():
    print("Loading CSV data...")
    # Load the CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # Define keywords for left-leaning claims
    left_keywords = [
        'reproductive rights', 'abortion', 'women\'s rights', 'lgbtq', 'gay rights',
        'trans rights', 'transgender', 'blm', 'black lives matter', 'racial justice',
        'police brutality', 'defund', 'climate', 'environment', 'green new deal',
        'healthcare', 'medicare for all', 'universal healthcare', 'living wage',
        'minimum wage', 'worker', 'union', 'labor rights', 'income inequality',
        'tax the rich', 'wealth tax', 'student debt', 'free college', 'immigration',
        'immigrant', 'refugee', 'asylum', 'ice', 'border', 'gun control', 'gun violence',
        'gun safety', 'palestine', 'palestinian', 'gaza', 'ceasefire', 'against genocide',
        'indigenous', 'native american', 'voting rights', 'gerrymandering', 'democracy',
        'progressive', 'liberal', 'socialist', 'social justice', 'equity', 'equality',
        'against capitalism', 'against pro-life', 'against deportations', 'against border security'
    ]

    # Helper function to check if a claim is left-leaning
    def is_left_leaning(claim_text):
        if not isinstance(claim_text, str):
            return False
        claim_lower = claim_text.lower()
        
        # Check for anti-abortion or anti-LGBT claims which should not be considered left-leaning
        if ('against' in claim_lower and 'abortion' in claim_lower) or \
           ('against' in claim_lower and 'pro-choice' in claim_lower) or \
           ('against' in claim_lower and 'reproductive rights' in claim_lower) or \
           ('against' in claim_lower and 'lgbt' in claim_lower) or \
           ('against' in claim_lower and 'gay' in claim_lower) or \
           ('against' in claim_lower and 'transgender' in claim_lower):
            return False
            
        # Check for left-leaning keywords
        return any(keyword.lower() in claim_lower for keyword in left_keywords)

    # Helper function to check if Trump or Musk is a target
    def targets_trump_or_musk(target_text):
        if not isinstance(target_text, str):
            return False
        target_lower = target_text.lower()
        return 'trump' in target_lower or 'musk' in target_lower

    # Filter for left-leaning claims based primarily on valence field
    print("Filtering for left-leaning protests using valence field as override...")
    
    # Create a new column that determines if an event is left-leaning
    df['is_left'] = df.apply(
        lambda row: True if row.get('valence') == 1 else  # If valence is 1, it's left-leaning
                   False if row.get('valence') == 2 else  # If valence is 2, it's not left-leaning
                   # If valence is not 1 or 2, use the original criteria
                   (is_left_leaning(row.get('claims_summary', '')) or 
                   targets_trump_or_musk(row.get('targets', ''))),
        axis=1
    )
    
    # Filter using the new column and date range
    left_protests = df[
        df['is_left'] & 
        (df['date'] >= '2025-01-20') & 
        (df['date'] <= '2025-03-31')
    ]
    
    # Drop the temporary column
    left_protests = left_protests.drop(columns=['is_left'])
    
    print(f"Found {len(left_protests)} left-leaning protests out of {len(df)} total")

    # Save filtered dataset
    output_file = 'ccc-phase3-left.csv'
    left_protests.to_csv(output_file, index=False)
    print(f"Saved filtered dataset to {output_file}")

    # Print some statistics
    print("\nTop 10 claims in filtered dataset:")
    claims_counts = left_protests['claims_summary'].value_counts().head(10)
    for i, (claim, count) in enumerate(claims_counts.items()):
        print(f"{i+1}. {claim}: {count}")

    print("\nTop 10 targets in filtered dataset:")
    targets_counts = left_protests['targets'].value_counts().head(10)
    for i, (target, count) in enumerate(targets_counts.items()):
        if isinstance(target, str):
            print(f"{i+1}. {target}: {count}")

if __name__ == "__main__":
    main()