from fastapi import Request
import logging
import time

async def log_requests(request: Request, call_next):
    logger = logging.getLogger("backend_server")
    start_time = time.time()

    # Process the request
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000 # to milliseconds
    process_time_formatted = f"{process_time:.2f}"

    # Handle cases where client info might be None (e.g., in tests)
    client_host = request.client.host if request.client else "unknown"
    client_port = request.client.port if request.client else 0

    # Log details as JSON
    log_dict = {
        "client_host": client_host,
        "client_port": client_port,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time_ms": process_time_formatted,
    }
    logger.info(log_dict)

    return response