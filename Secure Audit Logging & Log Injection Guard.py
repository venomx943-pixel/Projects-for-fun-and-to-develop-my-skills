import logging
import re
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure secure file logging
logging.basicConfig(
    filename="security_audit.log",
    level=logging.INFO,
    format="%(asctime)s - SECURITY_AUDIT - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Secure Audited AI Service",
    description="A FastAPI service equipped with a tamper-resistant audit logging middleware.",
    version="1.0.0"
)

class SecureAuditLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware to monitor incoming requests and securely log audit trails
    while neutralizing Log Injection (Log Forging) attacks.
    """
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        method = request.method

        # Security check: Sanitize client-controlled inputs against Log Injection (CRLF / Newline injection)
        sanitized_ip = re.sub(r'[\r\n]', '_', client_ip)
        sanitized_path = re.sub(r'[\r\n]', '_', path)
        sanitized_method = re.sub(r'[\r\n]', '_', method)

        # Construct safe audit log message
        audit_message = f"IP: {sanitized_ip} | Method: {sanitized_method} | Path: {sanitized_path}"
        
        # Write securely to the audit log file
        logging.info(audit_message)

        # Proceed with the request execution
        response = await call_next(request)
        return response

# Register the audit middleware into FastAPI
app.add_middleware(SecureAuditLogMiddleware)

@app.get("/audit-test")
def audit_test_endpoint():
    """
    An endpoint that triggers audit logging validation.
    """
    return {
        "status": "Success",
        "message": "Request successfully processed and recorded in the secure audit trail."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)