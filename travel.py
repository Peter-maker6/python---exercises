from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from models.destination import Base as DestinationBase
from models.experience import Base as ExperienceBase
from models.testimonial import Base as TestimonialBase
from models.gallery import Base as GalleryBase
from models.contact import Base as ContactBase
from routes import destinations, experiences, testimonials, gallery, contact
import os
from dotenv import load_dotenv

load_dotenv()

# Create all tables
DestinationBase.metadata.create_all(bind=engine)
ExperienceBase.metadata.create_all(bind=engine)
TestimonialBase.metadata.create_all(bind=engine)
GalleryBase.metadata.create_all(bind=engine)
ContactBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wanderlust Tours & Travels API",
    description="Backend API for Wanderlust Tours & Travels website",
    version="1.0.0"
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(destinations.router)
app.include_router(experiences.router)
app.include_router(testimonials.router)
app.include_router(gallery.router)
app.include_router(contact.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Wanderlust Tours & Travels API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
