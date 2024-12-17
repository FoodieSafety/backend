# test_middleware.py
import asyncio

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import Request, Response
import logging
import time
from starlette.datastructures import URL, Headers

async def create_mock_request(
        method="GET",
        url="/test",
        client_host="127.0.0.1",
        client_port=12345
):
    """Helper function to create a mock Request object"""
    scope = {
        "type": "http",
        "method": method,
        "path": url,
        "headers": Headers({}),
        # Add client info to scope instead of trying to set it later
        "client": (client_host, client_port),
        "scheme": "http",
        "server": ("testserver", 80),
        "root_path": "",
        "query_string": b"",
    }

    request = Request(scope)

    # Mock the URL
    mock_url = Mock()
    mock_url.path = url
    # Use object.__setattr__ to bypass the property
    object.__setattr__(request, '_url', mock_url)

    return request


@pytest.mark.asyncio
async def test_log_requests_basic():
    """Test basic logging functionality with all information available"""
    # Create mock request
    request = await create_mock_request()

    # Create mock response
    response = Response(content="test", status_code=200)
    call_next = AsyncMock(return_value=response)

    # Mock the logger
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        # Call the middleware
        from backend.middlewares.logging_middleware import log_requests
        result = await log_requests(request, call_next)

        # Verify the response is passed through
        assert result == response

        # Verify logger was called with correct data
        mock_logger.info.assert_called_once()
        log_dict = mock_logger.info.call_args[0][0]

        # Check log dictionary contents
        assert log_dict["client_host"] == "127.0.0.1"
        assert log_dict["client_port"] == 12345
        assert log_dict["method"] == "GET"
        assert log_dict["path"] == "/test"
        assert log_dict["status_code"] == 200
        assert isinstance(float(log_dict["process_time_ms"]), float)


@pytest.mark.asyncio
async def test_log_requests_no_client():
    """Test logging when client information is not available"""
    # Create mock request without client info by setting client to None in scope
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": Headers({}),
        "client": None,  # This will make request.client None
        "scheme": "http",
        "server": ("testserver", 80),
        "root_path": "",
        "query_string": b"",
    }
    request = Request(scope)

    # Mock the URL
    mock_url = Mock()
    mock_url.path = "/test"
    object.__setattr__(request, '_url', mock_url)

    # Create mock response
    response = Response(content="test", status_code=404)
    call_next = AsyncMock(return_value=response)

    # Mock the logger
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        # Call the middleware
        from backend.middlewares.logging_middleware import log_requests
        result = await log_requests(request, call_next)

        # Verify logger was called with correct data
        mock_logger.info.assert_called_once()
        log_dict = mock_logger.info.call_args[0][0]

        # Check log dictionary contents
        assert log_dict["client_host"] == "unknown"
        assert log_dict["client_port"] == 0
        assert log_dict["status_code"] == 404


@pytest.mark.asyncio
async def test_log_requests_different_methods():
    """Test logging with different HTTP methods"""
    for method in ["POST", "PUT", "DELETE", "PATCH"]:
        request = await create_mock_request(method=method)
        response = Response(content="test", status_code=200)
        call_next = AsyncMock(return_value=response)

        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            from backend.middlewares.logging_middleware import log_requests
            await log_requests(request, call_next)

            log_dict = mock_logger.info.call_args[0][0]
            assert log_dict["method"] == method


@pytest.mark.asyncio
async def test_log_requests_process_time():
    """Test that process time is calculated and formatted correctly"""
    request = await create_mock_request()

    # Create a delayed response that accepts the request parameter
    async def delayed_response(request):
        await asyncio.sleep(0.1)
        return Response(content="test", status_code=200)

    call_next = AsyncMock(side_effect=delayed_response)

    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        from backend.middlewares.logging_middleware import log_requests
        await log_requests(request, call_next)

        log_dict = mock_logger.info.call_args[0][0]
        process_time = float(log_dict["process_time_ms"])

        # Process time should be greater than 100ms (due to sleep)
        assert process_time > 100
        # Verify it's formatted to 2 decimal places
        assert len(str(process_time).split('.')[-1]) == 2


@pytest.mark.asyncio
async def test_log_requests_error_handling():
    """Test logging when call_next raises an exception"""
    request = await create_mock_request()

    # Mock call_next to raise an exception, accepting request parameter
    async def raise_error(request):
        raise ValueError("Test error")

    call_next = AsyncMock(side_effect=raise_error)

    with patch("logging.getLogger") as mock_get_logger:
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        from backend.middlewares.logging_middleware import log_requests
        # Verify the exception is propagated
        with pytest.raises(ValueError):
            await log_requests(request, call_next)

        # Verify no log was created (since response wasn't generated)
        mock_logger.info.assert_not_called()