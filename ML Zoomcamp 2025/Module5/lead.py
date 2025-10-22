from pydantic import BaseModel

class LeadPost(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float
