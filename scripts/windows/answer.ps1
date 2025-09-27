param([string]$Query = "what is the sterile changeover checklist?", [string]$Role = "Operator")
$body = @{ query = $Query; user_role = $Role } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/v1/answer -ContentType 'application/json' -Body $body

