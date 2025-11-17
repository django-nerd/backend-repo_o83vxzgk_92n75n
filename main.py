import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import MenuItem, Reservation, Testimonial, RestaurantInfo

app = FastAPI(title="Hungarian Restaurant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hungarian Restaurant API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "Unknown"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Seed minimal restaurant info if not present
@app.get("/api/info", response_model=RestaurantInfo)
def get_info():
    # Try to get one info document
    try:
        docs = get_documents("restaurantinfo", {}, limit=1)
        if docs:
            d = docs[0]
            return RestaurantInfo(**{k: v for k, v in d.items() if k in RestaurantInfo.model_fields})
    except Exception:
        pass
    # default fallback content
    return RestaurantInfo(
        name="Paprika & Pálinka",
        tagline="Authentic Hungarian flavors in the heart of the city",
        address="60 Andrassy Ave",
        city="Budapest",
        phone="(+36) 1 234 5678",
        email="hello@paprikapalinka.hu",
        hours=[
            "Mon-Thu: 12:00 - 22:00",
            "Fri-Sat: 12:00 - 23:00",
            "Sun: 12:00 - 21:00",
        ],
        hero_image="https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1400&auto=format&fit=crop"
    )

@app.get("/api/menu", response_model=List[MenuItem])
def get_menu():
    try:
        items = get_documents("menuitem")
        if items:
            result = []
            for it in items:
                data = {k: v for k, v in it.items() if k in MenuItem.model_fields}
                result.append(MenuItem(**data))
            return result
    except Exception:
        pass
    # default starter menu
    return [
        MenuItem(name="Gulyásleves (Goulash)", description="Traditional beef and vegetable soup with paprika.", price=9.5, category="Starters", image="https://images.unsplash.com/photo-1604908176997-4316c2b17178?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Chicken Paprikash", description="Tender chicken in creamy paprika sauce served with nokedli.", price=15.0, category="Mains", image="https://images.unsplash.com/photo-1559620192-032c4bc4674e?q=80&w=1200&auto=format&fit=crop"),
        MenuItem(name="Fisherman's Soup (Halászlé)", description="Spicy river fish soup from the Danube.", price=13.0, category="Mains"),
        MenuItem(name="Dobos Torte", description="Layered sponge cake with chocolate buttercream and caramel glaze.", price=6.5, category="Desserts", image="https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?q=80&w=1200&auto=format&fit=crop"),
    ]

class ReservationRequest(Reservation):
    pass

@app.post("/api/reservations")
def create_reservation(reservation: ReservationRequest):
    try:
        inserted_id = create_document("reservation", reservation)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/testimonials", response_model=List[Testimonial])
def get_testimonials():
    try:
        docs = get_documents("testimonial")
        if docs:
            return [Testimonial(**{k: v for k, v in d.items() if k in Testimonial.model_fields}) for d in docs]
    except Exception:
        pass
    return [
        Testimonial(name="Anna", rating=5, comment="The best goulash I've ever had!"),
        Testimonial(name="Bence", rating=4, comment="Authentic flavors and cozy atmosphere."),
        Testimonial(name="Éva", rating=5, comment="Dobos torte was heavenly!")
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
