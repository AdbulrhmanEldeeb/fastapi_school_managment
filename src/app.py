from fastapi import FastAPI 
from routes import base_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
# This is useful for making the API accessible from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow access from any origin. Restrict this in production for security.
    allow_credentials=True,  # Allows cookies or authentication credentials in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all types of headers (e.g., Content-Type, Authorization)
)

# Include the base_router which contains all the API routes for student management
app.include_router(base_router)
