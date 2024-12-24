import pandas as pd

def load_data(file_path="data/properties.csv"):
    """Loads property data from a CSV file."""
    data = pd.read_csv(file_path)
    return data
