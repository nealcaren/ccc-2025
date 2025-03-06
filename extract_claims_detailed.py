import pandas as pd
import json
from pathlib import Path
from collections import Counter

def main():
    print("Loading CSV data...")
    # Load the CSV data with Latin encoding
    df = pd.read_csv('ccc-phase3-public.csv', encoding='latin1')
    print(f"Loaded {len(df)} events from CSV")

    # Extract claims and split by semicolons
    print("Analyzing claims_summary field...")
    claims_series = df['claims_summary'].fillna('Unknown')
    
    # Split all claims by semicolons and create a flat list
    all_claims = []
    for claim_text in claims_series:
        # Split by semicolons and strip whitespace
        if claim_text != 'Unknown':
            individual_claims = [c.strip() for c in claim_text.split(';')]
            all_claims.extend(individual_claims)
    
    # Count frequencies using Counter
    claims_counter = Counter(all_claims)
    
    # Convert to DataFrame for easier analysis
    claims_df = pd.DataFrame({
        'claim': list(claims_counter.keys()),
        'count': list(claims_counter.values())
    }).sort_values('count', ascending=False)
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    output_file = 'data/claims_detailed.csv'
    claims_df.to_csv(output_file, index=False)
    print(f"Saved {len(claims_df)} unique individual claims to {output_file}")
    
    # Also save as JSON for potential web use
    claims_dict = dict(zip(claims_df['claim'], claims_df['count']))
    with open('data/claims_detailed.json', 'w') as f:
        json.dump(claims_dict, f)
    
    # Print top 20 claims
    print("\nTop 20 individual claims:")
    for i, (claim, count) in enumerate(zip(claims_df['claim'][:20], claims_df['count'][:20])):
        print(f"{i+1}. {claim}: {count}")
    
    # Create a summary table showing claim categories
    print("\nAnalyzing claim categories...")
    
    # Define some common claim categories to look for
    categories = {
        'trump': ['trump', 'donald trump'],
        'palestine': ['palestine', 'gaza', 'palestinian'],
        'women': ['women', 'reproductive', 'abortion'],
        'climate': ['climate', 'environment'],
        'lgbtq': ['lgbtq', 'gay', 'trans'],
        'immigration': ['immigra', 'border', 'migrant'],
        'racial_justice': ['racial justice', 'black lives', 'blm'],
        'gun_control': ['gun', 'firearm'],
        'healthcare': ['healthcare', 'health care', 'medicare'],
        'economic': ['economic', 'wage', 'poverty', 'inequality']
    }
    
    # Count claims in each category
    category_counts = {}
    for category, keywords in categories.items():
        count = sum(1 for claim in all_claims if any(keyword.lower() in claim.lower() for keyword in keywords))
        category_counts[category] = count
    
    # Save category counts
    category_df = pd.DataFrame({
        'category': list(category_counts.keys()),
        'count': list(category_counts.values())
    }).sort_values('count', ascending=False)
    
    category_df.to_csv('data/claim_categories.csv', index=False)
    print(f"Saved claim categories to data/claim_categories.csv")
    
    # Print category counts
    print("\nClaim categories:")
    for i, (category, count) in enumerate(zip(category_df['category'], category_df['count'])):
        print(f"{category}: {count} claims")

if __name__ == "__main__":
    main()
