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
import logging

# Set up logging at the top of the file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_server():
    logger.info("Starting mock NTFY server...")
    thread = threading.Thread(
        target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000)
    )
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Wait for server to start
    logger.info("Mock NTFY server is running")
    yield
    logger.info("Shutting down mock NTFY server...")
    # Server will be terminated when test ends

@pytest.fixture
def test_config():
    logger.info("Creating test configuration file...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        config = {
            "log_file": "tests/test.log",
            "keywords": ["ERROR"],
            "ntfy": {
                "topic": "test",
                "server": "http://localhost:8000",
                "priority": 3
            }
        }
        json.dump(config, f)
        logger.info(f"Test configuration created at: {f.name}")
        return f.name

def test_log_monitoring(mock_server, test_config):
    logger.info("Starting log monitoring test...")
    
    # Create test log file
    logger.info("Creating test log file...")
    with open("tests/test.log", "w") as f:
        f.write("Initial log\n")
    
    # Initialize monitor
    logger.info("Initializing LogMonitor...")
    monitor = LogMonitor(test_config)

    # Simulate log update with error
    logger.info("Writing ERROR message to log file...")
    with open("tests/test.log", "a") as f:
        f.write("This is an ERROR message\n")

    # Trigger monitor
    logger.info("Triggering file modification event...")
    monitor.on_modified(type('Event', (), {'src_path': 'tests/test.log'})())

    # Check if notification was sent
    logger.info("Waiting for notification to be sent...")
    time.sleep(1)
    
    logger.info("Checking notifications...")
    response = requests.get("http://localhost:8000/test/notifications")
    notifications = response.json()
    
    logger.info(f"Received {len(notifications)} notifications")
    assert len(notifications) == 1, "Expected exactly one notification"
    assert "ERROR" in notifications[0]["message"], "Notification should contain ERROR message"
    logger.info("Test completed successfully")
