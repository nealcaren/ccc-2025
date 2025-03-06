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
    print("Analyzing claims_summary field for political orientation...")
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
    
    # Define keywords for anti-Trump claims
    anti_trump_keywords = [
        'against trump', 'against donald trump', 'anti-trump', 'anti trump', 
        'trump abuse', 'trump\'s abuse', 'against president trump', 
        'impeach', 'resist', 'resistance', 'not my president'
    ]
    
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
    
    # Define keywords for right-leaning claims
    right_keywords = [
        'pro-trump', 'support trump', 'maga', 'america first', 'stop the steal',
        'election fraud', 'pro-life', 'against abortion', 'traditional values',
        'family values', 'religious freedom', 'second amendment', 'gun rights',
        'border security', 'illegal immigration', 'law and order', 'blue lives matter',
        'support police', 'anti-socialism', 'anti-communism', 'lower taxes',
        'small government', 'deregulation', 'free market', 'capitalism',
        'against cancel culture', 'free speech', 'anti-woke', 'anti-crt',
        'parental rights', 'school choice', 'against mask mandates', 'against vaccine mandates',
        'medical freedom', 'pro-israel', 'in solidarity with israel', 'against antisemitism'
    ]
    
    # Flag claims
    claims_df['anti_trump'] = claims_df['claim'].apply(
        lambda x: any(keyword.lower() in x.lower() for keyword in anti_trump_keywords)
    )
    
    claims_df['left_leaning'] = claims_df['claim'].apply(
        lambda x: any(keyword.lower() in x.lower() for keyword in left_keywords)
    )
    
    claims_df['right_leaning'] = claims_df['claim'].apply(
        lambda x: any(keyword.lower() in x.lower() for keyword in right_keywords)
    )
    
    # Extract anti-Trump claims
    anti_trump_claims = claims_df[claims_df['anti_trump']].sort_values('count', ascending=False)
    
    # Extract left-leaning claims
    left_claims = claims_df[claims_df['left_leaning'] & ~claims_df['right_leaning']].sort_values('count', ascending=False)
    
    # Extract right-leaning claims
    right_claims = claims_df[claims_df['right_leaning'] & ~claims_df['left_leaning']].sort_values('count', ascending=False)
    
    # Extract ambiguous claims (flagged as both left and right)
    ambiguous_claims = claims_df[claims_df['left_leaning'] & claims_df['right_leaning']].sort_values('count', ascending=False)
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    anti_trump_claims.to_csv('data/anti_trump_claims.csv', index=False)
    left_claims.to_csv('data/left_leaning_claims.csv', index=False)
    right_claims.to_csv('data/right_leaning_claims.csv', index=False)
    ambiguous_claims.to_csv('data/ambiguous_claims.csv', index=False)
    
    # Print top anti-Trump claims
    print("\nTop 50 Anti-Trump Claims:")
    for i, (claim, count) in enumerate(zip(anti_trump_claims['claim'][:50], anti_trump_claims['count'][:50])):
        print(f"{i+1}. {claim}: {count}")
    
    # Print top left-leaning claims
    print("\nTop 50 Left-Leaning Claims:")
    for i, (claim, count) in enumerate(zip(left_claims['claim'][:50], left_claims['count'][:50])):
        print(f"{i+1}. {claim}: {count}")
    
    # Print top right-leaning claims
    print("\nTop 20 Right-Leaning Claims:")
    for i, (claim, count) in enumerate(zip(right_claims['claim'][:20], right_claims['count'][:20])):
        print(f"{i+1}. {claim}: {count}")
    
    # Print summary
    print("\nSummary:")
    print(f"Total unique claims: {len(claims_df)}")
    print(f"Anti-Trump claims: {len(anti_trump_claims)}")
    print(f"Left-leaning claims: {len(left_claims)}")
    print(f"Right-leaning claims: {len(right_claims)}")
    print(f"Ambiguous claims: {len(ambiguous_claims)}")
    
    # Calculate total mentions
    anti_trump_mentions = anti_trump_claims['count'].sum()
    left_mentions = left_claims['count'].sum()
    right_mentions = right_claims['count'].sum()
    ambiguous_mentions = ambiguous_claims['count'].sum()
    total_mentions = claims_df['count'].sum()
    
    print(f"\nTotal claim mentions: {total_mentions}")
    print(f"Anti-Trump mentions: {anti_trump_mentions} ({anti_trump_mentions/total_mentions*100:.2f}%)")
    print(f"Left-leaning mentions: {left_mentions} ({left_mentions/total_mentions*100:.2f}%)")
    print(f"Right-leaning mentions: {right_mentions} ({right_mentions/total_mentions*100:.2f}%)")
    print(f"Ambiguous mentions: {ambiguous_mentions} ({ambiguous_mentions/total_mentions*100:.2f}%)")

if __name__ == "__main__":
    main()
