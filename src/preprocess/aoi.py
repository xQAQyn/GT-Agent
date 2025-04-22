import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
import joblib
import time

# --- Configuration ---
INPUT_CSV_PATH = 'data/LaDe/pickup/pickup_cq.csv'  # Your large CSV file
LON_COL = 'lng'
LAT_COL = 'lat'
AOI_COL = 'aoi_id'

OUTPUT_TREE_PATH = 'processed_data/pickup_cq/aoi/aoi_balltree.joblib' # Where to save the BallTree object
OUTPUT_IDS_PATH = 'processed_data/pickup_cq/aoi/aoi_ids.joblib'     # Where to save the corresponding AOI IDs

# --- Preprocessing ---
print("Starting AOI data preprocessing...")
start_time = time.time()

try:
    # 1. Load the full dataset
    print(f"Loading full dataset from {INPUT_CSV_PATH}...")
    df = pd.read_csv(INPUT_CSV_PATH, usecols=[LON_COL, LAT_COL, AOI_COL])
    df.dropna(subset=[LON_COL, LAT_COL, AOI_COL], inplace=True)
    print(f"Loaded {len(df)} valid points.")

    # 2. Calculate representative point (centroid) for each AOI
    print("Calculating centroids for each AOI...")
    # Group by AOI and calculate the mean lat/lon for each group
    # Important: Ensure AOI_COL is suitable for grouping (e.g., integer or string)
    # If AOI_COL might be float, convert it first: df[AOI_COL] = df[AOI_COL].astype(int) 
    centroids = df.groupby(AOI_COL)[[LAT_COL, LON_COL]].mean().reset_index()
    print(f"Calculated centroids for {len(centroids)} unique AOIs.")

    # 3. Prepare data for BallTree
    # Get the AOI IDs in the order corresponding to the centroid coordinates
    aoi_ids_ordered = centroids[AOI_COL].values
    # Get the centroid coordinates [latitude, longitude]
    centroid_coords_deg = centroids[[LAT_COL, LON_COL]].values
    # Convert centroid coordinates to radians for Haversine distance
    centroid_coords_rad = np.radians(centroid_coords_deg)

    # 4. Build the BallTree
    print("Building BallTree on centroids...")
    tree = BallTree(centroid_coords_rad, metric='haversine')
    print("BallTree built successfully.")

    # 5. Persist the BallTree and the ordered AOI IDs
    print(f"Saving BallTree to {OUTPUT_TREE_PATH}...")
    joblib.dump(tree, OUTPUT_TREE_PATH)
    
    print(f"Saving ordered AOI IDs to {OUTPUT_IDS_PATH}...")
    joblib.dump(aoi_ids_ordered, OUTPUT_IDS_PATH)

    end_time = time.time()
    print(f"\nPreprocessing complete.")
    print(f"Saved BallTree for {len(aoi_ids_ordered)} AOIs.")
    print(f"Total time: {end_time - start_time:.2f} seconds.")

except FileNotFoundError:
    print(f"Error: Input CSV file not found at {INPUT_CSV_PATH}")
except KeyError as e:
    print(f"Error: Column '{e}' not found in {INPUT_CSV_PATH}. Check configuration.")
except Exception as e:
    print(f"An unexpected error occurred during preprocessing: {e}")