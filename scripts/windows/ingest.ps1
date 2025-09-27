param([string]$Path = "./docs/sop.txt")
$body = @{ path = $Path } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/v1/ingest -ContentType 'application/json' -Body $body

