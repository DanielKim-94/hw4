$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $project '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { throw "Python environment not found at $python" }

$backend = Test-NetConnection 127.0.0.1 -Port 8015 -WarningAction SilentlyContinue
if (-not $backend.TcpTestSucceeded) {
  Start-Process -FilePath $python -WorkingDirectory (Join-Path $project 'backend') -ArgumentList '-m','uvicorn','main:app','--host','127.0.0.1','--port','8015' -WindowStyle Hidden
}

$frontend = Test-NetConnection 127.0.0.1 -Port 5175 -WarningAction SilentlyContinue
if (-not $frontend.TcpTestSucceeded) {
  Start-Process -FilePath 'npm.cmd' -WorkingDirectory $project -ArgumentList 'run','dev','--','--host','127.0.0.1','--port','5175' -WindowStyle Hidden
}

Start-Sleep -Seconds 2
Write-Host 'Campus Customs is starting at http://127.0.0.1:5175/'
Write-Host 'Products: http://127.0.0.1:5175/products'
