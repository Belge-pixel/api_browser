from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NavigationSchema(BaseModel):
    """
    Schema for navigation data.
    """
    # id: int = Field(..., description="Unique identifier for the navigation item")
    ip_address: str = Field(..., description="ip address of the navigation item")
    mac_address: str = Field(..., description="mac address of the navigation item in the list")
    url: str = Field(..., description="URL associated with the navigation item")
    timestamp: Optional[datetime] = Field(..., description="Timestamp of the navigation data")