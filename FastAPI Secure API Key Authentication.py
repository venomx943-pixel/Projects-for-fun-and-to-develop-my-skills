from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import secrets

app = FastAPI(
    title="Secure Authenticated AI Service",
    description="A FastAPI service protected with cryptographic API key authentication.",
    version="1.0.0"
)

# Simulated secure master API key for production
PRODUCTION_API_KEY = "sk-secure-ai-production-key-2026"
API_KEY_HEADER_NAME = "X-API-Key"

# Define the security header schema
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Validates incoming API keys using constant-time comparison to prevent timing attacks
    and unauthorized model access.
    """
    # Security check: Ensure the header is actually provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security Alert: Missing API Key in request headers."
        )
    
    # Security check: Constant-time string comparison to prevent side-channel timing exploits
    if not secrets.compare_digest(api_key, PRODUCTION_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Alert: Invalid API Key provided. Access denied."
        )
        
    return api_key

@app.post("/secure-predict")
def secure_model_prediction(authorized_key: str = Security(verify_api_key)):
    """
    A protected AI endpoint that requires cryptographic authentication clearance.
    """
    return {
        "status": "Success",
        "message": "Authentication verified successfully. Model inference authorized."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)