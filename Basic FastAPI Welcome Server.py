from fastapi import FastAPI, HTTPException, Query
import re
import uvicorn

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Basic Welcome Service",
    description="A foundational FastAPI server for testing web endpoints and input safety.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """
    Root endpoint to check server health status.
    """
    return {
        "status": "Active",
        "message": "Welcome to the FastAPI training server."
    }

@app.get("/welcome")
def welcome_user(name: str = Query(..., min_length=2, max_length=50, description="User name")):
    """
    Welcomes a user with input sanitization against injection or unexpected characters.
    """
    # Security check: Ensure name contains only English letters and spaces to prevent injection
    if not re.match("^[A-Za-z\\s]+$", name):
        raise HTTPException(
            status_code=400,
            detail="Invalid input: Name must contain only English letters and spaces."
        )
    
    sanitized_name = name.strip()
    
    return {
        "status": "Success",
        "greeting": f"Hello, {sanitized_name}! Welcome aboard."
    }

if __name__ == "__main__":
   
    # Run the server locally for testing purposes
    # Use terminal command: uvicorn filename:app --reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)