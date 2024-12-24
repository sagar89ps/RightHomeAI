import numpy as np
from typing import Dict, Any

def analyze_property_risks(property_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Comprehensive risk analysis for a property
    
    :param property_data: Dictionary containing property details
    :return: Dictionary of risk scores
    """
    risk_factors = {
        'market_volatility': _calculate_market_volatility(property_data),
        'price_stability': _assess_price_stability(property_data),
        'location_risk': _evaluate_location_risk(property_data['location']),
        'sustainability_risk': _calculate_sustainability_risk(property_data),
        'amenities_impact': _assess_amenities_impact(property_data)
    }
    
    # Overall risk score
    risk_factors['overall_risk'] = np.mean(list(risk_factors.values()))
    
    return {k: round(v, 2) for k, v in risk_factors.items()}

def _calculate_market_volatility(property_data: Dict[str, Any]) -> float:
    """Simulate market volatility risk assessment"""
    base_price = property_data['price']
    volatility_factor = np.random.uniform(0.5, 1.5)
    return min(max(abs(base_price * volatility_factor / 100000), 0), 10)

def _assess_price_stability(property_data: Dict[str, Any]) -> float:
    """Assess price stability based on property characteristics"""
    stability_score = 10 - abs(property_data['price'] / 50000 - 5)
    return min(max(stability_score, 0), 10)

def _evaluate_location_risk(location: str) -> float:
    """Simulate location-based risk assessment"""
    location_risk_map = {
        'Austin': 3.0,
        'Dallas': 2.5,
        'Houston': 4.0,
        'San Antonio': 3.5
    }
    return location_risk_map.get(location, 5.0)

def _calculate_sustainability_risk(property_data: Dict[str, Any]) -> float:
    """Convert sustainability score to risk"""
    return 10 - property_data['sustainability']

def _assess_amenities_impact(property_data: Dict[str, Any]) -> float:
    """Assess how amenities might affect property risk"""
    return property_data['amenities'] / 2