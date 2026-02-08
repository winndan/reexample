from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- For Sale ---

class ForSaleCreate(BaseModel):
    title: str
    price: str
    price_numeric: float = 0
    price_label: str = "Gross Price"
    description: str
    location: str
    beds: str
    baths: str
    area: str
    img_url: str = ""
    featured: bool = False


class ForSaleUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    price_numeric: Optional[float] = None
    price_label: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    beds: Optional[str] = None
    baths: Optional[str] = None
    area: Optional[str] = None
    img_url: Optional[str] = None
    featured: Optional[bool] = None


class ForSaleResponse(BaseModel):
    id: str
    title: str
    price: str
    price_numeric: float
    price_label: str
    description: str
    location: str
    beds: str
    baths: str
    area: str
    img_url: str
    featured: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# --- Pre-Selling ---

class PreSellingCreate(BaseModel):
    title: str
    price: str
    price_numeric: float = 0
    price_label: str = "Starting Price"
    description: str
    location: str
    beds: str
    baths: str
    area: str
    img_url: str = ""
    developer: str
    turnover: str


class PreSellingUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    price_numeric: Optional[float] = None
    price_label: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    beds: Optional[str] = None
    baths: Optional[str] = None
    area: Optional[str] = None
    img_url: Optional[str] = None
    developer: Optional[str] = None
    turnover: Optional[str] = None


class PreSellingResponse(BaseModel):
    id: str
    title: str
    price: str
    price_numeric: float
    price_label: str
    description: str
    location: str
    beds: str
    baths: str
    area: str
    img_url: str
    developer: str
    turnover: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# --- For Lease ---

class ForLeaseCreate(BaseModel):
    title: str
    price: str
    price_numeric: float = 0
    price_label: str = "/ month"
    description: str
    location: str
    beds: str
    baths: str
    area: str
    img_url: str = ""
    furnishing: str = "Unfurnished"
    featured: bool = False


class ForLeaseUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    price_numeric: Optional[float] = None
    price_label: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    beds: Optional[str] = None
    baths: Optional[str] = None
    area: Optional[str] = None
    img_url: Optional[str] = None
    furnishing: Optional[str] = None
    featured: Optional[bool] = None


class ForLeaseResponse(BaseModel):
    id: str
    title: str
    price: str
    price_numeric: float
    price_label: str
    description: str
    location: str
    beds: str
    baths: str
    area: str
    img_url: str
    furnishing: str
    featured: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# --- Contact Messages ---

class ContactMessageCreate(BaseModel):
    name: str
    email: str
    phone: str
    interest: str = ""
    message: str


class ContactMessageResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    interest: str
    message: str
    is_read: bool
    created_at: Optional[datetime] = None
