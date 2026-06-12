# Codex app-server task scheduler registration on shun-sensei PC
$ErrorActionPreference = 'Continue'
$taskName = 'Codex AppServer'
Write-Host '=== Codex app-server install (shun-sensei) ==='

# Stop existing codex app-server processes
Get-CimInstance Win32_Process -Filter "Name = 'codex.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*app-server*' } | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    Write-Host ('Killed existing codex.exe PID=' + $_.ProcessId)
}

# Find codex.exe
$codex = (Get-Command codex.exe -ErrorAction SilentlyContinue).Source
if (-not $codex) {
    Write-Host 'FAIL: codex.exe not found in PATH'
    exit 1
}
Write-Host ('codex path: ' + $codex)

# Cleanup existing task
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host ('Removed existing task: ' + $taskName)
}

# Register new task (logon trigger + boot trigger)
$action = New-ScheduledTaskAction -Execute $codex -Argument 'app-server --listen ws://127.0.0.1:18080'
$trigger1 = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$trigger2 = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Days 0)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Limited -LogonType Interactive
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($trigger1, $trigger2) -Settings $settings -Principal $principal -Description 'Codex CLI app-server (localhost:18080) for SSH-tunneled remote access' | Out-Null
Write-Host ('Task registered: ' + $taskName)

# Start now
Start-ScheduledTask -TaskName $taskName
Start-Sleep -Seconds 4

# Verify
Write-Host ''
Write-Host '=== Status ==='
Get-ScheduledTaskInfo -TaskName $taskName | Select-Object LastTaskResult, LastRunTime, NumberOfMissedRuns | Format-Table -AutoSize

Write-Host '=== Port 18080 ==='
$conn = Get-NetTCPConnection -LocalPort 18080 -State Listen -ErrorAction SilentlyContinue
if ($conn) {
    $conn | Select-Object LocalAddress, LocalPort, State, OwningProcess | Format-Table -AutoSize
    $proc = Get-Process -Id $conn[0].OwningProcess -ErrorAction SilentlyContinue
    Write-Host ('Process: ' + $proc.ProcessName + ' PID=' + $proc.Id)
} else {
    Write-Host 'No listener on 18080 yet (may take a moment)'
}

Write-Host ''
Write-Host '=== Healthz ==='
try {
    $r = Invoke-WebRequest -Uri http://127.0.0.1:18080/healthz -UseBasicParsing -TimeoutSec 5
    Write-Host ('HTTP ' + $r.StatusCode + ' OK')
} catch {
    Write-Host ('FAIL: ' + $_.Exception.Message)
}
