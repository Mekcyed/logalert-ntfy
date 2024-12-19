# logalert-ntfy
Monitoring logfiles for keywords - Sending notifications via [ntfy.sh](ntfy.sh)

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
