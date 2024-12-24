# def weighted_score(properties, weights):
#     """Calculates weighted scores for properties."""
#     scores = []
#     for _, row in properties.iterrows():
#         score = sum(row[param] * weights.get(param, 1) for param in weights)
#         scores.append((row['name'], score))
#     return sorted(scores, key=lambda x: x[1], reverse=True)


import pandas as pd
from typing import Optional, List, Tuple

def advanced_property_filter(
    properties: pd.DataFrame,
    price_range: Optional[Tuple[float, float]] = None,
    location: Optional[str] = None,
    min_walkability: Optional[float] = None,
    min_amenities: Optional[float] = None,
    sustainability_threshold: Optional[float] = None
) -> pd.DataFrame:
    """
    Advanced filtering for properties based on multiple criteria
    
    :param properties: Input DataFrame of properties
    :param price_range: Tuple of (min_price, max_price)
    :param location: Specific city or neighborhood
    :param min_walkability: Minimum walkability score
    :param min_amenities: Minimum amenities score
    :param sustainability_threshold: Minimum sustainability score
    :return: Filtered DataFrame
    """
    filtered_properties = properties.copy()
    
    if price_range:
        filtered_properties = filtered_properties[
            (filtered_properties['price'] >= price_range[0]) & 
            (filtered_properties['price'] <= price_range[1])
        ]
    
    if location:
        filtered_properties = filtered_properties[
            filtered_properties['location'] == location
        ]
    
    if min_walkability:
        filtered_properties = filtered_properties[
            filtered_properties['walkability'] >= min_walkability
        ]
    
    if min_amenities:
        filtered_properties = filtered_properties[
            filtered_properties['amenities'] >= min_amenities
        ]
    
    if sustainability_threshold:
        filtered_properties = filtered_properties[
            filtered_properties['sustainability'] >= sustainability_threshold
        ]
    
    return filtered_properties

def weighted_score(properties: pd.DataFrame, weights: dict) -> List[Tuple[str, float]]:
    """
    Calculate weighted scores for properties
    
    :param properties: Input DataFrame of properties
    :param weights: Dictionary of parameter weights
    :return: Sorted list of (property_name, score) tuples
    """
    scores = []
    for _, row in properties.iterrows():
        # Normalize score calculation
        score = sum(
            row[param] * weight / 10 * 100  # Normalize to 0-100 scale
            for param, weight in weights.items()
        ) / sum(weights.values())
        
        scores.append((row['name'], round(score, 2)))
    
    return sorted(scores, key=lambda x: x[1], reverse=True)