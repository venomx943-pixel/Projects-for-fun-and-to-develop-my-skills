import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Header, status

app = FastAPI(
    title="HMAC Secure AI Gateway",
    description="A FastAPI service protected with cryptographic HMAC request signatures.",
    version="1.0.0"
)

# Shared secret key between the legitimate client and the AI server
SHARED_SECRET_KEY = b"elite_ai_security_shared_secret_2026"

def verify_hmac_signature(request_body: bytes, received_signature: str) -> bool:
    """
    Computes cryptographic HMAC-SHA256 signature and compares it safely
    with the received signature to prevent tampering.
    """
    if not received_signature:
        return False

    # Compute expected HMAC signature using the shared secret and request payload
    computed_signature = hmac.new(
        SHARED_SECRET_KEY, 
        request_body, 
        hashlib.sha256
    ).hexdigest()

    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_signature, received_signature)

@app.post("/secure-infer")
async def secure_ai_inference(request: Request, x_signature: str = Header(None)):
    """
    An AI inference endpoint protected by cryptographic request signatures.
    """
    # Security check: Ensure signature header is present
    if not x_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security Alert: Missing HMAC signature header."
        )

    # Read the raw request body bytes
    body_bytes = await request.body()

    # Security verification: Check if the payload was altered or unauthenticated
    if not verify_hmac_signature(body_bytes, x_signature):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Security Alert: HMAC signature verification failed. Request tampered or invalid."
        )

    return {
        "status": "Success",
        "message": "HMAC signature verified. Request integrity confirmed. Proceeding with AI inference."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)