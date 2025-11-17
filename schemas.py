"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (you can keep or remove if not needed)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Hungarian Restaurant Schemas
class MenuItem(BaseModel):
    name: str = Field(..., description="Dish name")
    description: str = Field(..., description="Short description of the dish")
    price: float = Field(..., ge=0, description="Price in local currency")
    category: str = Field(..., description="Category such as Starters, Mains, Desserts")
    image: Optional[str] = Field(None, description="Public image URL")
    spicy: Optional[bool] = Field(False, description="Whether the dish is spicy")
    vegetarian: Optional[bool] = Field(False, description="Vegetarian friendly")

class Reservation(BaseModel):
    name: str = Field(..., description="Guest full name")
    email: str = Field(..., description="Contact email")
    phone: str = Field(..., description="Contact phone number")
    date: str = Field(..., description="Reservation date YYYY-MM-DD")
    time: str = Field(..., description="Reservation time HH:MM")
    party_size: int = Field(..., ge=1, le=20, description="Number of guests")
    notes: Optional[str] = Field(None, description="Special requests")

class Testimonial(BaseModel):
    name: str = Field(..., description="Customer name")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(..., description="Their comment")
    avatar: Optional[str] = Field(None, description="Avatar image URL")

class RestaurantInfo(BaseModel):
    name: str = Field(..., description="Restaurant name")
    tagline: str = Field(..., description="Short tagline")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    phone: str = Field(..., description="Phone number")
    email: str = Field(..., description="Contact email")
    hours: List[str] = Field(default_factory=list, description="Opening hours lines")
    hero_image: Optional[str] = Field(None, description="Hero background image URL")
