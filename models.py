from pydantic import BaseModel, field_validator

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    
class ScrapeResult(BaseModel):
    text: str
    markdown: str
    
class ShoppingResult(BaseModel):
    title: str 
    source: str
    link: str
    price: str | int | float
    delivery: str
    imageUrl: str
    rating: str | int | float
    ratingCount: str | int | float
    offers: str
    productId: str
    position: str | int  # Allow both int and str

    # Convert numerical fields to strings automatically
    @field_validator("rating", "ratingCount", "position", mode="before")
    @classmethod
    def convert_to_string(cls, value):
        return str(value) if isinstance(value, (int, float)) else value