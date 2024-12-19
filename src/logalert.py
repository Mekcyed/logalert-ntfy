#!/usr/bin/env python3
import json
import requests
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import time
from typing import Dict, List
from urllib.parse import urlparse
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logalert.log')
    ]
)
logger = logging.getLogger(__name__)

class ConfigValidator:
    @staticmethod
    def validate_config(config: Dict) -> None:
        # Check required fields
        required_fields = ['log_file', 'keywords', 'ntfy']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")

        # Validate log_file
        if not os.path.exists(config['log_file']):
            raise FileNotFoundError(f"Log file not found: {config['log_file']}")
        if not os.access(config['log_file'], os.R_OK):
            raise PermissionError(f"No read permission for log file: {config['log_file']}")

        # Validate keywords
        if not isinstance(config['keywords'], list) or not config['keywords']:
            raise ValueError("Keywords must be a non-empty list")

        # Validate ntfy config
        ntfy_config = config['ntfy']
        required_ntfy_fields = ['server', 'topic', 'priority']
        for field in required_ntfy_fields:
            if field not in ntfy_config:
                raise ValueError(f"Missing required ntfy field: {field}")

        # Validate server URL
        try:
            result = urlparse(ntfy_config['server'])
            if not all([result.scheme, result.netloc]):
                raise ValueError
        except ValueError:
            raise ValueError(f"Invalid ntfy server URL: {ntfy_config['server']}")

        # Validate priority
        if not isinstance(ntfy_config['priority'], int) or not (1 <= ntfy_config['priority'] <= 5):
            raise ValueError("Priority must be an integer between 1 and 5")

class LogMonitor(FileSystemEventHandler):
    def __init__(self, config_path: str):
        try:
            self.config = self._load_config(config_path)
            ConfigValidator.validate_config(self.config)
            logger.info("Configuration loaded and validated successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LogMonitor: {str(e)}")
            raise

    def _load_config(self, config_path: str) -> Dict:
        try:
            with open(config_path) as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def _send_notification(self, message: str) -> None:
        ntfy_config = self.config['ntfy']
        url = f"{ntfy_config['server']}/{ntfy_config['topic']}"

        try:
            response = requests.post(
                url,
                data=message.encode(encoding='utf-8'),
                headers={
                    "Priority": str(ntfy_config['priority'])
                },
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Notification sent successfully: {message[:100]}...")
        except requests.Timeout:
            logger.error(f"Timeout sending notification to {url}")
            raise
        except requests.RequestException as e:
            logger.error(f"Failed to send notification: {str(e)}")
            raise

    def on_modified(self, event) -> None:
        if event.src_path == self.config['log_file']:
            try:
                with open(self.config['log_file']) as f:
                    lines = f.readlines()[-10:]
                    for line in lines:
                        if any(keyword in line for keyword in self.config['keywords']):
                            try:
                                self._send_notification(line)
                            except Exception as e:
                                logger.error(f"Failed to process notification: {str(e)}")
            except Exception as e:
                logger.error(f"Error reading log file: {str(e)}")

def main():
    try:
        logger.info("Starting LogAlert monitoring service")
        monitor = LogMonitor('config.json')
        observer = Observer()
        observer.schedule(monitor, path='.', recursive=False)
        observer.start()
        logger.info("File monitoring started")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            observer.stop()
        observer.join()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
