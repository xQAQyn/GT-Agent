import numpy as np
from sklearn.neighbors import BallTree # Needed for loading, even if not building
import joblib
import os # To check if files exist

class FastGeoAOIMapper:
    """
    Loads a pre-built BallTree (based on AOI centroids) and maps 
    new longitude/latitude points to the nearest AOI ID efficiently.
    """
    def __init__(self, tree_path='processed_data/pickup_cq/aoi/aoi_balltree.joblib', ids_path='processed_data/pickup_cq/aoi/aoi_ids.joblib'):
        """
        Initializes the mapper by loading the pre-built index from disk.

        Args:
            tree_path (str): Path to the saved BallTree object (.joblib).
            ids_path (str): Path to the saved ordered AOI IDs (.joblib).
        """
        self.tree = None
        self.aoi_ids = None

        print("Initializing FastGeoAOIMapper...")
        if not os.path.exists(tree_path):
            print(f"Error: BallTree file not found at {tree_path}")
            print("Please run the preprocessing script first.")
            raise FileNotFoundError(f"BallTree file not found: {tree_path}")
            
        if not os.path.exists(ids_path):
            print(f"Error: AOI IDs file not found at {ids_path}")
            print("Please run the preprocessing script first.")
            raise FileNotFoundError(f"AOI IDs file not found: {ids_path}")

        try:
            print(f"Loading BallTree from {tree_path}...")
            self.tree = joblib.load(tree_path)
            
            print(f"Loading AOI IDs from {ids_path}...")
            self.aoi_ids = joblib.load(ids_path)
            
            if self.tree is None or self.aoi_ids is None:
                 raise ValueError("Failed to load required data from disk.")

            # Basic sanity check (optional but recommended)
            if self.tree.data.shape[0] != len(self.aoi_ids):
                 raise ValueError("Mismatch between number of points in BallTree and number of AOI IDs.")

            print(f"Mapper initialized successfully with {len(self.aoi_ids)} AOIs.")

        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")
            self.tree = None # Ensure inconsistent state is cleared
            self.aoi_ids = None
            raise # Re-raise the exception after logging

    def get_aoi_id(self, lon, lat):
        """
        Finds the AOI ID for a given longitude and latitude using the loaded index.

        Args:
            lon (float): Longitude of the query point.
            lat (float): Latitude of the query point.

        Returns:
            The AOI ID corresponding to the nearest AOI centroid, 
            or None if the mapper wasn't initialized correctly or an error occurs.
        """
        if self.tree is None or self.aoi_ids is None:
            print("Error: Mapper is not properly initialized.")
            return None
            
        try:
            # Convert query point to radians, order: [latitude, longitude]
            query_point_rad = np.radians([[lat, lon]]) 

            # Query the loaded BallTree for the nearest neighbor (k=1)
            # Returns distances and indices
            dist, ind = self.tree.query(query_point_rad, k=1)
            
            # Get the index of the nearest centroid
            nearest_index = ind[0][0]
            
            # Look up the corresponding AOI ID
            nearest_aoi_id = self.aoi_ids[nearest_index]
            
            return nearest_aoi_id
            
        except Exception as e:
            print(f"An error occurred during query for ({lon}, {lat}): {e}")
            return None
