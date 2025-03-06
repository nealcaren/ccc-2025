import pandas as pd
from pathlib import Path

def main():
    print("Loading tagged CSV data...")
    # Check if tagged data exists, otherwise use the filtered data
    if Path('ccc-phase3-left-tagged.csv').exists():
        df = pd.read_csv('ccc-phase3-left-tagged.csv', encoding='latin1')
        print(f"Loaded {len(df)} tagged events from CSV")
    else:
        df = pd.read_csv('ccc-phase3-left.csv', encoding='latin1')
        print(f"Loaded {len(df)} events from CSV (untagged)")
        print("Please run analyze_protest_tags.py first to generate tags")
        return

    # Extract all claims and split by semicolons
    print("Extracting claims and their tags...")
    
    # Get all tag columns
    tag_columns = [col for col in df.columns if col.startswith('tag_')]
    
    # Create a list to store all claims and their tags
    claims_with_tags = []
    
    # Process each row
    for _, row in df.iterrows():
        claims_text = row['claims_summary']
        if not isinstance(claims_text, str) or claims_text == 'Unknown':
            continue
            
        # Split claims by semicolons
        individual_claims = [claim.strip() for claim in claims_text.split(';')]
        
        # Get tags for this event
        tags = {}
        for tag_col in tag_columns:
            if row[tag_col] == 1:
                # Convert tag_gaza to Gaza
                tag_name = tag_col[4:].replace('_', ' ').title().replace('Lgbt', 'LGBT').replace('Lgbtplus', 'LGBT+')
                tags[tag_name] = 1
        
        # Add each claim with its tags
        for claim in individual_claims:
            claim_entry = {'claim': claim}
            claim_entry.update(tags)
            claims_with_tags.append(claim_entry)
    
    # Convert to DataFrame
    claims_df = pd.DataFrame(claims_with_tags)
    
    # Fill NaN values with 0 for tag columns
    for tag_col in tags.keys():
        if tag_col in claims_df.columns:
            claims_df[tag_col] = claims_df[tag_col].fillna(0)
    
    # Save to CSV
    Path('data').mkdir(exist_ok=True)
    output_file = 'data/claims_with_tags.csv'
    claims_df.to_csv(output_file, index=False)
    print(f"Saved {len(claims_df)} claims with their tags to {output_file}")
    
    # Create a summary of claims by tag
    print("\nSummary of claims by tag:")
    for tag in tags.keys():
        if tag in claims_df.columns:
            tag_count = claims_df[tag].sum()
            print(f"{tag}: {int(tag_count)} claims")
    
    # Also count unique events by tag from the original dataframe
    print("\nSummary of events by tag:")
    for tag_col in tag_columns:
        tag_name = tag_col[4:].replace('_', ' ').title().replace('Lgbt', 'LGBT').replace('Lgbtplus', 'LGBT+')
        event_count = df[tag_col].sum()
        print(f"{tag_name}: {int(event_count)} events ({event_count/len(df)*100:.2f}%)")

if __name__ == "__main__":
    main()
