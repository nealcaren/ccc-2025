#!/bin/bash

# Build script for protest data processing pipeline
echo "Starting build process..."

# Step 1: Filter for left-leaning protests
echo "Step 1: Filtering for left-leaning protests..."
uv run filter_left_protests.py

# Step 2: Analyze and tag the protests
echo "Step 2: Analyzing and tagging protests..."
uv run analyze_protest_tags.py

# Step 3: Generate dashboard data files
echo "Step 3: Generating dashboard data files..."
uv run process_data.py

# Step 4: Generate issue summary
echo "Step 4: Generating issue summary..."
uv run extract_issue_summary.py

echo "Build process completed successfully!"
