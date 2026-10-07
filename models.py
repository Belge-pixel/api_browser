from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base


class Navigation(Base):
    __tablename__ = "navigation"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    url = Column(String, nullable=False)
    wifi_credentials = Column(String, nullable=True)
    wifi_ssid = Column(String, nullable=True)
    wifi_password = Column(String, nullable=True)
    timestamp = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    ) 
