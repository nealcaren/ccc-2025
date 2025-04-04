import pandas as pd
import json
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load CSV
file_path = "ccc-phase3-public.csv"
logging.info(f"Loading data from {file_path}")
df = pd.read_csv(file_path, dtype=str, encoding='latin')  # Read all columns as strings initially to handle missing values
logging.info(f"Initial dataframe shape: {df.shape}")

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
    k: v for k, v in {
        "locality": row["locality"] if pd.notna(row["locality"]) else None,
        "state": row["state"] if pd.notna(row["state"]) else None,
        "county": row["resolved_county"] if pd.notna(row["resolved_county"]) else None,
        "lat": row["lat"] if pd.notna(row["lat"]) else None,
        "lon": row["lon"] if pd.notna(row["lon"]) else None
    }.items() if v is not None and not (isinstance(v, float) and np.isnan(v))
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
        return {k: remove_empty(v) for k, v in d.items() 
                if v not in [None, [], {}, ""] and not (isinstance(v, float) and np.isnan(v))}
    elif isinstance(d, list):
        return [remove_empty(v) for v in d 
                if v not in [None, [], {}, ""] and not (isinstance(v, float) and np.isnan(v))]
    else:
        return d

# Apply removal of empty values
logging.info("Before removing empty values, sample row:")
if json_output["rows"]:
    logging.info(json.dumps(json_output["rows"][0], indent=2))

# Count items before cleaning
before_count = sum(len(row) for row in json_output["rows"])
logging.info(f"Total fields before cleaning: {before_count}")

json_output = remove_empty(json_output)

# Count items after cleaning
after_count = sum(len(row) for row in json_output["rows"])
logging.info(f"Total fields after cleaning: {after_count}")
logging.info(f"Removed {before_count - after_count} empty fields")

# Save to file
output_path = "ccc-phase3-public-optimized.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=2)

logging.info(f"Optimized JSON saved to {output_path}")
print(f"Optimized JSON saved to {output_path}")
