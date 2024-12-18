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
