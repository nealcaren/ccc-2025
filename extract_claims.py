import pandas as pd
import json
from pathlib import Path

def main():
    print("Loading CSV data...")
    # Load the CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # Extract claims and count frequencies
    print("Analyzing claims...")
    claims_series = df['claims_summary'].fillna('Unknown')
    
    # Some claims are combined with semicolons, so we'll split them
    all_claims = []
    for claim_text in claims_series:
        # Split by semicolons and strip whitespace
        individual_claims = [c.strip() for c in claim_text.split(';')]
        all_claims.extend(individual_claims)
    
    # Count frequencies
    claims_counts = pd.Series(all_claims).value_counts().reset_index()
    claims_counts.columns = ['claim', 'count']
    
    # Save to CSV
    output_file = 'data/claims_counts.csv'
    claims_counts.to_csv(output_file, index=False)
    print(f"Saved {len(claims_counts)} unique claims to {output_file}")

    # Also create a JSON version for potential web use
    claims_dict = dict(zip(claims_counts['claim'], claims_counts['count']))
    with open('data/claims_counts.json', 'w') as f:
        json.dump(claims_dict, f)
    
    # Print top 10 claims
    print("\nTop 10 claims:")
    for i, (claim, count) in enumerate(zip(claims_counts['claim'][:10], claims_counts['count'][:10])):
        print(f"{i+1}. {claim}: {count}")

if __name__ == "__main__":
    main()
