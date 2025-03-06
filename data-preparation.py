import pandas as pd
import json
import numpy as np
from datetime import datetime

# Load the dataset
df = pd.read_csv('ccc-phase3-public.csv', encoding='latin')

# Basic cleaning
# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract month and year for aggregation
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['month_year'] = df['date'].dt.strftime('%Y-%m')

# Handle missing values for key columns
df['size_mean'] = df['size_mean'].fillna(0)
df['event_type'] = df['event_type'].fillna('unknown')
df['claims_summary'] = df['claims_summary'].fillna('unspecified')

# Create simplified claim categories
def categorize_claims(claim_text):
    if pd.isna(claim_text):
        return 'Other'
    
    claim_text = claim_text.lower()
    
    categories = {
        'trump': ['trump', 'president trump'],
        'women': ['women', 'reproductive', 'abortion'],
        'palestine': ['palestine', 'gaza', 'palestinian'],
        'climate': ['climate', 'environmental'],
        'lgbtq': ['lgbtq', 'queer', 'trans'],
        'immigration': ['immigra', 'migrant', 'border'],
        'racial justice': ['black lives', 'racial justice', 'blm'],
        'labor': ['labor', 'worker', 'union', 'wage']
    }
    
    for category, keywords in categories.items():
        if any(keyword in claim_text for keyword in keywords):
            return category
    
    return 'Other'

df['claim_category'] = df['claims_summary'].apply(categorize_claims)

# Prepare event type data for visualization
event_type_counts = df['event_type'].value_counts().reset_index()
event_type_counts.columns = ['event_type', 'count']
event_type_counts = event_type_counts.head(10)  # Top 10 event types

# Prepare state data for map visualization
state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['state', 'count']

# Prepare monthly protest counts
monthly_counts = df.groupby('month_year').size().reset_index()
monthly_counts.columns = ['month_year', 'count']
monthly_counts = monthly_counts.sort_values('month_year')

# Prepare claim categories data
claim_category_counts = df['claim_category'].value_counts().reset_index()
claim_category_counts.columns = ['category', 'count']

# Prepare top protest locations
location_counts = df['locality'].value_counts().head(10).reset_index()
location_counts.columns = ['locality', 'count']

# Create a summary object with key statistics
summary_stats = {
    'total_protests': len(df),
    'total_states': df['state'].nunique(),
    'avg_protest_size': round(df['size_mean'].mean(), 2),
    'largest_protest_size': df['size_mean'].max(),
    'most_common_event_type': df['event_type'].value_counts().index[0],
    'most_frequent_location': df['locality'].value_counts().index[0],
    'date_range': {
        'start': df['date'].min().strftime('%Y-%m-%d'),
        'end': df['date'].max().strftime('%Y-%m-%d')
    }
}

# Create export objects for the dashboard
dashboard_data = {
    'summary': summary_stats,
    'event_types': event_type_counts.to_dict(orient='records'),
    'states': state_counts.to_dict(orient='records'),
    'monthly_counts': monthly_counts.to_dict(orient='records'),
    'claim_categories': claim_category_counts.to_dict(orient='records'),
    'top_locations': location_counts.to_dict(orient='records')
}

# Export to JSON for the web dashboard
with open('dashboard_data.json', 'w') as f:
    json.dump(dashboard_data, f)

print("Data preparation complete. Dashboard data saved to dashboard_data.json")

# Optional: Generate a more detailed dataset for advanced visualization
# Create top organization data
org_counts = df['organizations'].str.split(';').explode().str.strip().value_counts().head(20).reset_index()
org_counts.columns = ['organization', 'count']

# Create claim co-occurrence matrix
def extract_claims(claim_text):
    if pd.isna(claim_text):
        return []
    
    claims = [c.strip() for c in claim_text.split(';')]
    return claims

df['claim_list'] = df['claims_summary'].apply(extract_claims)
all_claims = [claim for sublist in df['claim_list'].dropna() for claim in sublist]
unique_claims = pd.Series(all_claims).value_counts().head(20).index.tolist()

claim_matrix = []
for claim1 in unique_claims:
    row = []
    for claim2 in unique_claims:
        # Count co-occurrences
        co_occur = sum(1 for claims in df['claim_list'] if claim1 in claims and claim2 in claims)
        row.append(co_occur)
    claim_matrix.append(row)

claim_network = {
    'nodes': [{'id': claim, 'group': 1} for claim in unique_claims],
    'links': []
}

for i, claim1 in enumerate(unique_claims):
    for j, claim2 in enumerate(unique_claims):
        if i != j and claim_matrix[i][j] > 0:
            claim_network['links'].append({
                'source': claim1,
                'target': claim2,
                'value': claim_matrix[i][j]
            })

# Export advanced data
advanced_data = {
    'top_organizations': org_counts.to_dict(orient='records'),
    'claim_network': claim_network
}

with open('advanced_dashboard_data.json', 'w') as f:
    json.dump(advanced_data, f)

print("Advanced data preparation complete. Advanced data saved to advanced_dashboard_data.json")
