from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas import NavigationSchema
from models import Navigation
from config import get_db, Base, engine
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


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


@app.post("/send")
def send_naviguation_data(
    data: NavigationSchema,
    db: Session = Depends(get_db)
) -> NavigationSchema:

    nav_data = Navigation(
        ip_address=data.ip_address,
        mac_address=data.mac_address,
        url=data.url,
        timestamp=(
            datetime.fromisoformat(str(data.timestamp))
            if data.timestamp
            else datetime.utcnow()
        )
    )

    db.add(nav_data)
    db.commit()
    db.refresh(nav_data)

    return nav_data


@app.get("/navigation-data")
def get_navigation_data(
    db: Session = Depends(get_db)
) -> List[NavigationSchema]:

    return db.query(Navigation).all()
