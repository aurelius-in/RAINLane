# Troubleshooting

- PowerShell JSON quoting: use hashtable + ConvertTo-Json or `.ps1` helpers
- Port conflicts: stop previous uvicorn `Stop-Process -Name python`
- Missing dependencies: `pip install -r requirements.txt`
