import pytest
import json
import tempfile
import os
from src.logalert import LogMonitor
import uvicorn
import threading
from tests.mock_ntfy import app
import requests
import time

@pytest.fixture
def mock_server():
    thread = threading.Thread(
        target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000)
    )
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Wait for server to start
    yield
    # Server will be terminated when test ends

@pytest.fixture
def test_config():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        config = {
            "log_file": "test.log",
            "keywords": ["ERROR"],
            "ntfy": {
                "topic": "test",
                "server": "http://localhost:8000",
                "priority": 3
            }
        }
        json.dump(config, f)
        return f.name

def test_log_monitoring(mock_server, test_config):
    # Create test log file
    with open("test.log", "w") as f:
        f.write("Initial log\n")

    # Initialize monitor
    monitor = LogMonitor(test_config)

    # Simulate log update with error
    with open("test.log", "a") as f:
        f.write("This is an ERROR message\n")

    # Trigger monitor
    monitor.on_modified(type('Event', (), {'src_path': 'test.log'})())

    # Check if notification was sent
    time.sleep(1)
    response = requests.get("http://localhost:8000/test/notifications")
    notifications = response.json()
    
    assert len(notifications) == 1
    assert "ERROR" in notifications[0]["message"]
