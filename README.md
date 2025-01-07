# logalert-ntfy
Monitoring logfiles for keywords - Sending notifications via [ntfy.sh](ntfy.sh)

[![Build and Release](https://github.com/Mekcyed/logalert-ntfy/actions/workflows/build.yml/badge.svg)](https://github.com/Mekcyed/logalert-ntfy/actions/workflows/build.yml)

The goals:
- Create a python executable to monitor system logs and call a ntfy endpoint (see here https://docs.ntfy.sh/publish/)
- Unittests should be created. For that we need a small fast api server to mimic the ntfy endpoint and see if the montoring works
- Config of the montoring should be done with a single json file which contains the log file path to look for, the Keywords to check and the data for the ntfy endpoint...

Nice to have features:
- working github CI/CD Pipline to run tests after pushs and creat a executable with pyinstaller and upload it to github.

## Folder Structure

The repository is organized as follows:

```
├── src
│    └── logalert.py
├── tests
│    └── test_logalert.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Configuration and Running Instructions

### Configuration

1. Create a `config.example.json` file in the root directory of the project with the following structure:

```json
config = {
            "log_file": "test.log",
            "keywords": ["ERROR"],
            "ntfy": {
                "topic": "test",
                "server": "http://localhost:8000",
                "priority": 3
            }
        }
```

- `log_file_path`: The path to the log file you want to monitor.
- `keywords`: A list of keywords to look for in the log file.
- `ntfy_endpoint`: The ntfy endpoint URL to send notifications to.

### Running Tests

1. Ensure you have the test dependencies installed:

```sh
pip install -r requirements.dev.txt
```

2. Run the tests with logging output:

```sh
pytest -v -s --log-cli-level=INFO
```

This will:
- Run all tests with verbose output (-v)
- Show print statements and logging in real-time (-s)
- Display INFO level logs during test execution (--log-cli-level=INFO)

You can also run tests without logging:

```sh
pytest
```

### Running the Python Executable

1. Ensure you have Python installed on your system.
2. Install the required dependencies using `pip`:

```sh
pip install -r requirements.txt
```

3. Run the Python executable:

```sh
python src/logalert.py
```

The script will start monitoring the specified log file for the given keywords and send notifications to the configured ntfy endpoint when any of the keywords are found in the log file.

## Running as a Service on Linux

### Creating a Virtual Environment and Installing Dependencies

1. Create a virtual environment:

```sh
python3 -m venv /path/to/new/virtual/environment
```

2. Activate the virtual environment:

```sh
source /path/to/new/virtual/environment/bin/activate
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

### Sample `systemd` Service File

Create a file named `logalert.service` with the following content:

```ini
[Unit]
Description=LogAlert Service
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/new/virtual/environment/bin/python /path/to/your/project/src/logalert.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Enabling and Starting the Service

1. Copy the `logalert.service` file to the systemd directory:

```sh
sudo cp logalert.service /etc/systemd/system/
```

2. Reload the systemd daemon to recognize the new service:

```sh
sudo systemctl daemon-reload
```

3. Enable the service to start on boot:

```sh
sudo systemctl enable logalert.service
```

4. Start the service:

```sh
sudo systemctl start logalert.service
```

5. Check the status of the service:

```sh
sudo systemctl status logalert.service
```
