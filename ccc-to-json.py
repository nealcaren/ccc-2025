import pandas as pd
import json

# Load CSV
file_path = "ccc-phase3-public.csv"
df = pd.read_csv(file_path, dtype=str, encoding='latin')  # Read all columns as strings initially to handle missing values

# Convert numeric fields to appropriate types
numeric_fields = ["lat", "lon", "size_low", "size_high", "size_mean", "valence", "conf"]
for field in numeric_fields:
    df[field] = pd.to_numeric(df[field], errors='coerce')

# Convert categorical fields to indexed values
categorical_fields = ["state", "event_type", "macroevent", "coder"]
category_maps = {field: {val: idx for idx, val in enumerate(df[field].dropna().unique())} for field in categorical_fields}
for field in categorical_fields:
    df[field] = df[field].map(category_maps[field])

# Combine source columns into a list and drop empty ones
source_columns = [col for col in df.columns if col.startswith("source")]
df["sources"] = df[source_columns].apply(lambda row: [s for s in row if pd.notna(s)], axis=1)
df.drop(columns=source_columns, inplace=True)  # Drop original source columns

# Nest location fields
df["location"] = df.apply(lambda row: {
    "locality": row["locality"] if pd.notna(row["locality"]) else None,
    "state": row["state"] if pd.notna(row["state"]) else None,
    "county": row["resolved_county"] if pd.notna(row["resolved_county"]) else None,
    "lat": row["lat"] if pd.notna(row["lat"]) else None,
    "lon": row["lon"] if pd.notna(row["lon"]) else None
}, axis=1)
df.drop(columns=["locality", "resolved_county", "lat", "lon"], inplace=True)

# Remove completely empty columns
df.dropna(axis=1, how="all", inplace=True)

# Convert DataFrame to JSON format
json_output = {
    "categories": category_maps,
    "rows": df.to_dict(orient="records")
}

# Function to remove empty values recursively
def remove_empty(d):
    """ Recursively remove empty values (None, NaN, empty lists, empty dicts). """
    if isinstance(d, dict):
        return {k: remove_empty(v) for k, v in d.items() if v not in [None, [], {}, ""]}
    elif isinstance(d, list):
        return [remove_empty(v) for v in d if v not in [None, [], {}, ""]]
    else:
        return d

# Apply removal of empty values
json_output = remove_empty(json_output)

# Save to file
output_path = "ccc-phase3-public-optimized.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=2)

print(f"Optimized JSON saved to {output_path}")
