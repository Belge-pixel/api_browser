from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas import NavigationSchema
from models import Navigation
from config import get_db, Base, engine
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import json


# Créer les tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API for sending navigation data"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def wifi_entry_to_dict(entry):
    """Convertit un élément de wifi_credentials (objet Pydantic ou dict) en dict simple."""
    if isinstance(entry, dict):
        return entry
    if hasattr(entry, "model_dump"):
        return entry.model_dump()
    if hasattr(entry, "dict"):  # fallback pydantic v1
        return entry.dict()
    return entry


@app.post("/send")
def send_naviguation_data(
    data: NavigationSchema,
    db: Session = Depends(get_db)
) -> NavigationSchema:
    # prepare wifi list and primary ssid/password
    wifi_list = [wifi_entry_to_dict(w) for w in (data.wifi_credentials or [])]
    wifi_json = json.dumps(wifi_list, ensure_ascii=False)

    # prefer explicit fields if client sent them, otherwise take first meaningful entry
    primary_ssid = data.wifi_ssid
    primary_password = data.wifi_password
    if not primary_ssid or not primary_password:
        try:
            for entry in wifi_list:
                ss = entry.get('ssid')
                pw = entry.get('password')
                if (not primary_ssid) and ss:
                    primary_ssid = ss
                if (not primary_password) and pw:
                    primary_password = pw
                if primary_ssid or primary_password:
                    break
        except Exception:
            pass

    nav_data = Navigation(
        ip_address=data.ip_address,
        mac_address=data.mac_address,
        url=data.url,
        wifi_credentials=wifi_json,
        wifi_ssid=primary_ssid,
        wifi_password=primary_password,
        timestamp=(
            datetime.fromisoformat(str(data.timestamp))
            if data.timestamp
            else datetime.utcnow()
        )
    )

    db.add(nav_data)
    db.commit()
    db.refresh(nav_data)
    try:
        nav_dict = {
            "id": nav_data.id,
            "ip_address": nav_data.ip_address,
            "mac_address": nav_data.mac_address,
            "url": nav_data.url,
            "timestamp": nav_data.timestamp,
            "wifi_credentials": json.loads(nav_data.wifi_credentials) if nav_data.wifi_credentials else [],
            "wifi_ssid": nav_data.wifi_ssid,
            "wifi_password": nav_data.wifi_password,
        }
    except Exception:
        nav_dict = {
            "id": nav_data.id,
            "ip_address": nav_data.ip_address,
            "mac_address": nav_data.mac_address,
            "url": nav_data.url,
            "timestamp": nav_data.timestamp,
            "wifi_credentials": [],
            "wifi_ssid": None,
            "wifi_password": None,
        }

    return nav_dict


@app.get("/navigation-data")
def get_navigation_data(
    db: Session = Depends(get_db)
) -> List[NavigationSchema]:
    rows = db.query(Navigation).all()
    result = []
    for r in rows:
        try:
            wifi = json.loads(r.wifi_credentials) if r.wifi_credentials else []
        except Exception:
            wifi = []
        result.append({
            "id": r.id,
            "ip_address": r.ip_address,
            "mac_address": r.mac_address,
            "url": r.url,
            "timestamp": r.timestamp,
            "wifi_credentials": wifi,
            "wifi_ssid": getattr(r, 'wifi_ssid', None),
            "wifi_password": getattr(r, 'wifi_password', None),
        })

    return result