$id = $args[0]
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/v1/provenance/$id" | ConvertTo-Json -Depth 5 | Write-Output

