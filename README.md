# CCC Phase 3 Data Dashboard

This dashboard visualizes protest event data from the CCC Phase 3 dataset.

## Setup Instructions

1. Make sure you have Python installed (Python 3.6 or higher recommended)

2. Install required dependencies:
   ```
   uv pip install pandas
   ```

3. Process the data:
   ```
   uv run process_data.py
   ```
   This will create JSON files in the `data` directory.

4. Serve the dashboard:
   You can use any static file server to serve the dashboard. Here are some options:

   - Using Python's http.server (for quick testing):
     ```
     python -m http.server
     ```

   - Using Node.js serve (if you have Node.js installed):
     ```
     npx serve
     ```

   - Using Netlify CLI (if you plan to deploy to Netlify):
     ```
     npx netlify-cli dev
     ```

5. Open your browser and navigate to the local server URL (typically http://localhost:8000 or similar)

## Deployment

To deploy this dashboard to Netlify or Vercel:

1. Process the data locally first to generate the JSON files
2. Create a new project on Netlify or Vercel
3. Upload the entire directory (including the generated data files)
4. Configure the build settings if needed

## Project Structure

- `process_data.py`: Script to process the CSV data and generate JSON files
- `index.html`: Main dashboard HTML
- `js/dashboard.js`: JavaScript code for the dashboard
- `data/`: Directory containing generated JSON files

## Data Source

The data comes from the CCC Phase 3 public dataset, which contains information about protest events in 2025.
