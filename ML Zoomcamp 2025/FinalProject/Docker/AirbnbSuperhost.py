from pydantic import BaseModel
from typing import Optional, Literal

class AirbnbSuperhost(BaseModel):
    # Host metrics
    host_response_rate: Optional[float] = None
    host_acceptance_rate: Optional[float] = None
    host_identity_verified: bool = False
    host_listings_count: Optional[float] = None
    host_is_superhost: bool = False
    calculated_host_listings_count: Optional[int] = None
    
    # Review scores
    review_scores_rating: Optional[float] = None
    review_scores_cleanliness: Optional[float] = None
    review_scores_communication: Optional[float] = None
    review_scores_accuracy: Optional[float] = None
    
    # Review metrics
    number_of_reviews: int = 0
    number_of_reviews_ltm: Optional[int] = None  # Last Twelve Months
    reviews_per_month: Optional[float] = None
    
    # Booking and availability
    instant_bookable: bool = False
    availability_30: Optional[int] = None
    
    # Categorical features
    room_type: Optional[Literal['entire_home_apt', 'private_room', 'shared_room', 'hotel_room']] = None
    neighbourhood: Optional[str] = None