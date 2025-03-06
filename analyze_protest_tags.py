import pandas as pd
import json
from pathlib import Path

def main():
    print("Loading filtered CSV data...")
    # Load the filtered left-leaning protests data with Latin encoding
    df = pd.read_csv('ccc-phase3-left.csv', encoding='latin1')
    print(f"Loaded {len(df)} left-leaning events from CSV")

    # Define tag categories and their keywords
    tag_categories = {
        'Gaza': ['gaza', 'palestinian', 'palestine', 'israel'],
        'Abortion': ['abortion', 'reproductive rights', 'pro-choice', 'women\'s rights'],
        'LGBT+': ['lgbt', 'lgbtq', 'gay', 'trans', 'transgender', 'queer'],
        'Environment': ['climate', 'environment', 'green', 'fossil fuel', 'pollution'],
        'Immigration': ['immigration', 'immigrant', ' ICE ', 'ICE,', 'ICE.', 'ICE:', 'border', 'migrant', 'refugee', 'asylum', 'deportation'],
        'Trump': ['trump', 'president trump', 'donald trump'],
        'Musk': ['musk', 'elon musk'],
        'Gun Control': ['gun', 'firearm', 'nra', 'second amendment'],
        'Healthcare': ['healthcare', 'health care', 'medicare', 'medicaid', 'universal health'],
        'Workers': ['worker', 'labor', 'union', 'wage', 'strike', 'fair pay'],
        'Racial Justice': ['racial justice', 'black lives', 'blm', 'police brutality', 'racism']
    }

    # Initialize tag columns
    for tag in tag_categories.keys():
        df[f'tag_{tag.lower().replace("+", "plus").replace(" ", "_")}'] = 0

    # Function to check if a claim contains any of the keywords for a tag
    def check_tag_keywords(claim_text, keywords, tag_name=None):
        if not isinstance(claim_text, str):
            return 0
        
        claim_lower = claim_text.lower()
        
        # Special handling for Gaza tag - exclude generic anti-war claims
        if tag_name == 'Gaza':
            # Only include claims that specifically mention Israel, Gaza, or Palestine
            # Exclude generic claims like "against all wars" or just "ceasefire" without context
            if ('gaza' in claim_lower or 'palestinian' in claim_lower or 
                'palestine' in claim_lower or 'israel' in claim_lower):
                return 1
            return 0
        
        # Special handling for Immigration tag
        if tag_name == 'Immigration':
            # Check for ICE with proper capitalization to avoid matching words ending in 'ice'
            if ' ICE ' in claim_text or 'ICE,' in claim_text or 'ICE.' in claim_text or 'ICE:' in claim_text:
                return 1
            
            # Check for other immigration-related keywords
            immigration_keywords = ['immigration', 'immigrant', 'border', 'migrant', 'refugee', 'asylum', 'deportation']
            return 1 if any(keyword.lower() in claim_lower for keyword in immigration_keywords) else 0
        
        # Standard keyword check for other tags
        return 1 if any(keyword.lower() in claim_lower for keyword in keywords) else 0

    # Function to check if a target contains any of the keywords for a tag
    def check_target_keywords(target_text, keywords):
        if not isinstance(target_text, str):
            return 0
        target_lower = target_text.lower()
        return 1 if any(keyword.lower() in target_lower for keyword in keywords) else 0

    # Apply tag detection to claims and targets
    print("Analyzing protest tags...")
    for tag, keywords in tag_categories.items():
        tag_col = f'tag_{tag.lower().replace("+", "plus").replace(" ", "_")}'
        
        # Check claims
        df[tag_col] = df['claims_summary'].apply(lambda x: check_tag_keywords(x, keywords, tag_name=tag))
        
        # For Trump and Musk, also check targets
        if tag in ['Trump', 'Musk']:
            df[tag_col] = df.apply(
                lambda row: 1 if row[tag_col] == 1 or check_target_keywords(row['targets'], keywords) else 0, 
                axis=1
            )

    # Calculate tag statistics - count events, not claims
    tag_stats = {}
    for tag in tag_categories.keys():
        tag_col = f'tag_{tag.lower().replace("+", "plus").replace(" ", "_")}'
        # Count unique events with this tag
        count = df[tag_col].sum()
        percentage = (count / len(df)) * 100
        tag_stats[tag] = {'count': int(count), 'percentage': float(percentage)}

    # Sort tags by count
    sorted_tags = sorted(tag_stats.items(), key=lambda x: x[1]['count'], reverse=True)
    
    # Save tag statistics to JSON
    Path('data').mkdir(exist_ok=True)
    with open('data/protest_tags.json', 'w') as f:
        json.dump({
            'tags': [tag for tag, _ in sorted_tags],
            'counts': [stats['count'] for _, stats in sorted_tags],
            'percentages': [stats['percentage'] for _, stats in sorted_tags]
        }, f)
    
    # Save tagged data back to CSV
    df.to_csv('ccc-phase3-left-tagged.csv', index=False)
    
    # Print tag statistics
    print("\nProtest Tag Statistics:")
    for tag, stats in sorted_tags:
        print(f"{tag}: {stats['count']} protests ({stats['percentage']:.2f}%)")
    
    print("\nData processing complete. Tag statistics saved to data/protest_tags.json")

if __name__ == "__main__":
    main()
