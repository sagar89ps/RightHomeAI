# from fastapi import FastAPI, Query
# from app.data_loader import load_data
# from app.recommender import weighted_score
# from app.visualizer import plot_scores

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Welcome to RightHomeAI!"}

# @app.get("/recommend")
# def recommend_properties(
#     price_weight: float = Query(1.0),
#     amenities_weight: float = Query(1.0),
#     sustainability_weight: float = Query(1.0),
#     walkability_weight: float = Query(1.0)
# ):
#     # Load data
#     properties = load_data()

#     # Define user weights
#     weights = {
#         "price": price_weight,
#         "amenities": amenities_weight,
#         "sustainability": sustainability_weight,
#         "walkability": walkability_weight
#     }

#     # Calculate scores
#     scores = weighted_score(properties, weights)

#     # Generate visualization
#     plot_scores(properties, scores)

#     return {"recommendations": scores}


from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.data_loader import load_data
from app.recommender import weighted_score, advanced_property_filter
from app.visualizer import plot_scores, generate_heatmap
from app.risk_analyzer import analyze_property_risks

app = FastAPI(
    title="RightHome.ai",
    description="AI-Powered Property Recommendation System",
    version="0.1.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PropertyFilterRequest(BaseModel):
    """
    Comprehensive property filter request model
    """
    price_range: Optional[tuple] = None
    location: Optional[str] = None
    min_walkability: Optional[float] = None
    min_amenities: Optional[float] = None
    sustainability_threshold: Optional[float] = None

class WeightedScoringRequest(BaseModel):
    """
    User-defined weight configuration for property scoring
    """
    price_weight: float = 1.0
    amenities_weight: float = 1.0
    sustainability_weight: float = 1.0
    walkability_weight: float = 1.0

@app.post("/recommend/advanced")
async def advanced_recommendation(
    filter_request: PropertyFilterRequest,
    scoring_request: WeightedScoringRequest
):
    """
    Advanced property recommendation endpoint with comprehensive filtering and scoring
    """
    try:
        # Load property data
        properties = load_data()

        # Apply advanced filtering
        filtered_properties = advanced_property_filter(
            properties, 
            price_range=filter_request.price_range,
            location=filter_request.location,
            min_walkability=filter_request.min_walkability,
            min_amenities=filter_request.min_amenities,
            sustainability_threshold=filter_request.sustainability_threshold
        )

        # Define weights dynamically
        weights = {
            "price": scoring_request.price_weight,
            "amenities": scoring_request.amenities_weight,
            "sustainability": scoring_request.sustainability_weight,
            "walkability": scoring_request.walkability_weight
        }

        # Calculate weighted scores
        scored_properties = weighted_score(filtered_properties, weights)

        # Generate visualizations
        plot_scores(filtered_properties, scored_properties)
        generate_heatmap(filtered_properties, scored_properties)

        # Perform risk analysis
        risk_analysis = [analyze_property_risks(prop) for prop in filtered_properties]

        return {
            "recommendations": scored_properties,
            "risk_analysis": risk_analysis,
            "total_properties_analyzed": len(filtered_properties)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Recommendation generation failed: {str(e)}"
        )

@app.get("/properties")
async def list_properties(
    location: Optional[str] = None,
    max_price: Optional[float] = None
):
    """
    Retrieve list of properties with optional filtering
    """
    properties = load_data()
    
    if location:
        properties = properties[properties['location'] == location]
    
    if max_price:
        properties = properties[properties['price'] <= max_price]
    
    return properties.to_dict(orient='records')

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy", "version": "0.1.0"}