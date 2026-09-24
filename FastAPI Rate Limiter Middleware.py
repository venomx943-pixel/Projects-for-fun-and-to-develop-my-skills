import time
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple

app = FastAPI(
    title="Secure Rate Limited API",
    description="A FastAPI service protected with a custom IP rate limiting middleware.",
    version="1.0.0"
)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to track and limit incoming requests per IP address
    to mitigate Denial of Service (DoS) and brute-force attacks.
    """
    def __init__(self, app, max_requests: int = 5, time_window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window
        # Dictionary to store client IP mapping: {ip: (request_count, window_start_time)}
        self.clients: Dict[str, Tuple[int, float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Security check & state tracking for the specific IP
        if client_ip not in self.clients:
            self.clients[client_ip] = (1, current_time)
        else:
            count, start_time = self.clients[client_ip]
            
            # Reset time window if expired
            if current_time - start_time > self.time_window:
                self.clients[client_ip] = (1, current_time)
            else:
                # Check if client exceeded maximum allowed requests within the window
                if count >= self.max_requests:
                    raise HTTPException(
                        status_code=429,
                        detail="Security Alert: Rate limit exceeded. Too many requests from this IP."
                    )
                # Increment request count
                self.clients[client_ip] = (count + 1, start_time)

        # Proceed with the request if within safe boundaries
        response = await call_next(request)
        return response

# Register the security middleware into the FastAPI application
app.add_middleware(RateLimitMiddleware, max_requests=3, time_window=60)

@app.get("/")
def protected_route():
    """
    A protected endpoint that requires rate-limiting clearance.
    """
    return {
        "status": "Success",
        "message": "Access granted to secure API endpoint."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)