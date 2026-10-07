from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List


class WifiCred(BaseModel):
    ssid: Optional[str] = None
    password: Optional[str] = None

class NavigationSchema(BaseModel):
    """
    Schema for navigation data.
    """
    # id: int = Field(..., description="Unique identifier for the navigation item")
    ip_address: str = Field(..., description="ip address of the navigation item")
    mac_address: str = Field(..., description="mac address of the navigation item in the list")
    url: str = Field(..., description="URL associated with the navigation item")
    timestamp: Optional[datetime] = Field(..., description="Timestamp of the navigation data")
    wifi_credentials: Optional[List[WifiCred]] = Field(None, description="List of wifi credentials (ssid/password)")
    wifi_ssid: Optional[str] = Field(None, description="Primary wifi ssid")
    wifi_password: Optional[str] = Field(None, description="Primary wifi password")