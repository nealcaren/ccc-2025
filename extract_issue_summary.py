import pandas as pd
import json
from pathlib import Path

def main():
    print("Generating protest issues summary...")
    
    # Check if tagged data exists
    if not Path('ccc-phase3-left-tagged.csv').exists():
        print("Error: Tagged data not found. Please run analyze_protest_tags.py first.")
        return
    
    # Load the tagged data
    df = pd.read_csv('ccc-phase3-left-tagged.csv', encoding='latin1')
    print(f"Loaded {len(df)} tagged events")
    
    # Get all tag columns
    tag_columns = [col for col in df.columns if col.startswith('tag_')]
    
    # Create a dictionary to store issue information
    issues_data = []
    
    # Process each tag
    for tag_col in tag_columns:
        # Convert tag_gaza to Gaza, and tag_musk to Musk/DOGE
        tag_name = tag_col[4:].replace('_', ' ').title().replace('Lgbt', 'LGBT').replace('Lgbtplus', 'LGBT+')
        if tag_name == 'Musk':
            tag_name = 'Musk/DOGE'
        
        # Count events with this tag
        event_count = df[tag_col].sum()
        event_percentage = (event_count / len(df)) * 100
        
        # Calculate total participants for this tag
        df['size_for_stats'] = df['size_mean'].fillna(11)
        participant_count = df[df[tag_col] == 1]['size_for_stats'].sum()
        total_participants = df['size_for_stats'].sum()
        participant_percentage = (participant_count / total_participants) * 100
        
        # Get keywords used for this tag
        keywords = []
        if tag_name == 'Gaza':
            keywords = ['gaza', 'palestinian', 'palestine', 'israel']
        elif tag_name == 'Abortion':
            keywords = ['abortion', 'reproductive rights', 'pro-choice', 'women\'s rights']
        elif tag_name == 'LGBT+':
            keywords = ['lgbt', 'lgbtq', 'gay', 'trans', 'transgender', 'queer']
        elif tag_name == 'Environment':
            keywords = ['climate', 'environment', 'green', 'fossil fuel', 'pollution']
        elif tag_name == 'Immigration':
            keywords = ['immigration', 'immigrant', 'ICE', 'border', 'migrant', 'refugee', 'asylum', 'deportation']
        elif tag_name == 'Trump':
            keywords = ['trump', 'president trump', 'donald trump']
        elif tag_name == 'Musk/DOGE':
            keywords = ['musk', 'elon musk', 'federal budget', 'budget cuts', 'doge']
        elif tag_name == 'Gun Control':
            keywords = ['gun', 'firearm', 'nra', 'second amendment']
        elif tag_name == 'Healthcare':
            keywords = ['healthcare', 'health care', 'medicare', 'medicaid', 'universal health']
        elif tag_name == 'Workers':
            keywords = ['worker', 'labor', 'union', 'wage', 'strike', 'fair pay']
        elif tag_name == 'Racial Justice':
            keywords = ['racial justice', 'black lives', 'blm', 'police brutality', 'racism']
        
        # Get top 5 claims for this tag
        top_claims = df[df[tag_col] == 1]['claims_summary'].value_counts().head(5).to_dict()
        
        # Add to issues data
        issues_data.append({
            'Issue': tag_name,
            'Event Count': int(event_count),
            'Event Percentage': round(event_percentage, 2),
            'Participant Count': int(participant_count),
            'Participant Percentage': round(participant_percentage, 2),
            'Keywords': ', '.join(keywords),
            'Top Claims': '; '.join([f"{claim} ({count})" for claim, count in top_claims.items()])
        })
    
    # Convert to DataFrame and sort by event count
    issues_df = pd.DataFrame(issues_data).sort_values('Event Count', ascending=False)
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    output_file = 'data/protest_issues_summary.csv'
    issues_df.to_csv(output_file, index=False)
    print(f"Saved protest issues summary to {output_file}")
    
    # Print summary
    print("\nProtest Issues Summary:")
    for _, row in issues_df.iterrows():
        print(f"{row['Issue']}: {row['Event Count']} events ({row['Event Percentage']}%), {row['Participant Count']} participants ({row['Participant Percentage']}%)")
    
    # Also create a more detailed CSV with all claims for each issue
    print("\nGenerating detailed claims by issue...")
    
    # Load the claims with tags data
    claims_with_tags_file = 'data/claims_with_tags.csv'
    if Path(claims_with_tags_file).exists():
        # Load the original events data to get the actual tag associations
        events_df = df.copy()
        
        # Load the claims data
        claims_df = pd.read_csv(claims_with_tags_file)
        
        # Count unique claims
        claim_counts = claims_df['claim'].value_counts().to_dict()
        
        # Create a mapping of claims to their actual issues
        claim_to_issues = {}
        
        # For each event in the original dataset
        for _, event in events_df.iterrows():
            claim = event['claims_summary']
            
            # Skip events without claims
            if pd.isna(claim):
                continue
                
            # Initialize this claim in our mapping if needed
            if claim not in claim_to_issues:
                claim_to_issues[claim] = set()
            
            # Get all tags for this event
            event_tags = set()
            for tag_col in tag_columns:
                if event[tag_col] == 1:
                    # Convert tag column name to readable issue name
                    issue_name = tag_col[4:].replace('_', ' ').title().replace('Lgbt', 'LGBT').replace('Lgbtplus', 'LGBT+')
                    if issue_name == 'Musk':
                        issue_name = 'Musk/DOGE'
                    event_tags.add(issue_name)
            
            # Check for federal budget cuts or Musk mentions to add Musk/DOGE tag
            target = str(event.get('target', '')).lower()
            claim_lower = str(claim).lower()
            
            if ('federal budget' in target or 'budget cut' in target or 
                'federal budget' in claim_lower or 'budget cut' in claim_lower or
                'musk' in target or 'musk' in claim_lower) and 'Musk/DOGE' not in event_tags:
                event_tags.add('Musk/DOGE')
            
            # Special handling for Trump tag
            if 'Trump' in event_tags:
                # Check if Trump is the only tag or if Trump is specifically mentioned in claim or target
                target = str(event.get('target', '')).lower()
                claim_lower = str(claim).lower()
                
                # If there are other tags and Trump isn't specifically the target or in claim, remove Trump tag
                if len(event_tags) > 1 and 'trump' not in target.lower() and 'trump' not in claim_lower:
                    event_tags.remove('Trump')
            
            # Add all remaining tags to this claim
            claim_to_issues[claim].update(event_tags)
        
        # Create detailed claims data
        detailed_claims = []
        for claim, issues in claim_to_issues.items():
            for issue in issues:
                detailed_claims.append({
                    'Claim': claim,
                    'Claim Count': claim_counts.get(claim, 0) if claim in claim_counts else 0,
                    'Issue': issue
                })
        
        # Convert to DataFrame and remove duplicates
        detailed_df = pd.DataFrame(detailed_claims).drop_duplicates()
        
        # Save to CSV
        output_file = 'data/detailed_claims_by_issue.csv'
        detailed_df.to_csv(output_file, index=False)
        print(f"Saved detailed claims by issue to {output_file}")
        
        # Create a simplified version with claims, counts, and their issues
        simplified_data = []
        for claim, issues in claim_to_issues.items():
            simplified_data.append({
                'Claim': claim,
                'Claim Count': claim_counts.get(claim, 0) if claim in claim_counts else 0,
                'Issues': ', '.join(sorted(issues))  # Join all issues for this claim
            })
        
        simplified_df = pd.DataFrame(simplified_data).sort_values('Claim Count', ascending=False)
        
        simplified_output_file = 'data/claims_issue_check.csv'
        simplified_df.to_csv(simplified_output_file, index=False)
        print(f"Saved simplified claims data to {simplified_output_file}")
    else:
        print(f"Warning: {claims_with_tags_file} not found. Run extract_claims_with_tags.py first to generate detailed claims data.")

if __name__ == "__main__":
    main()
