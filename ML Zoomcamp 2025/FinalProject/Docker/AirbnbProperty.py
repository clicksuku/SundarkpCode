from pydantic import BaseModel
from typing import Optional

class AirbnbProperty(BaseModel):
    # Host information
    host_response_rate: Optional[float] = None
    host_acceptance_rate: Optional[float] = None
    host_is_superhost: bool = False
    host_identity_verified: bool = False

    # Property details
    accommodates: int
    bedrooms: int
    bathrooms: float
    beds: int
    
    # Reviews
    number_of_reviews: int = 0
    review_scores_rating: Optional[float] = None

    # Booking details
    minimum_nights: int
    instant_bookable: bool = False
    
    
    # Room type flags (one-hot encoded)
    entire_home_apt: bool = False
    private_room: bool = False
    shared_room: bool = False
    hotel_room: bool = False
    
    # Neighborhood flags (one-hot encoded)
    leopoldstadt: bool = False
    others: bool = False
    margareten: bool = False
    brigittenau: bool = False
    landstrae: bool = False
    ottakring: bool = False
    rudolfsheim_fnfhaus: bool = False
    neubau: bool = False
    alsergrund: bool = False
    meidling: bool = False
    favoriten: bool = False


