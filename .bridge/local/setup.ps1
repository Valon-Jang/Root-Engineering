$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$repo = 'Valon-Jang/Root-Engineering'
$branch = 'naver-local-persistent-20260830'
$root = Join-Path $env:LOCALAPPDATA 'NaverMailBridge'
$runnerDir = Join-Path $root 'actions-runner'
$startup = [Environment]::GetFolderPath('Startup')
$rawBase = "https://raw.githubusercontent.com/$repo/$branch/.bridge/local"
New-Item -ItemType Directory -Force -Path $root, $runnerDir | Out-Null

function Refresh-Path {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$machine;$user"
}

function Ensure-Gh {
    $x = Get-Command gh -ErrorAction SilentlyContinue
    if ($x) { return $x.Source }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'GitHub CLI is missing and winget is unavailable.' }
    & winget install --id GitHub.cli -e --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw 'GitHub CLI installation failed.' }
    Refresh-Path
    $x = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $x) { throw 'GitHub CLI was installed but gh.exe was not found. Reopen PowerShell and run setup again.' }
    return $x.Source
}

function Find-Python {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        try {
            $candidate = ((& $py.Source -3 -c "import sys;print(sys.executable)") | Select-Object -Last 1).Trim()
            if ($candidate -and (Test-Path $candidate)) { return $candidate }
        } catch {}
    }
    $p = Get-Command python -ErrorAction SilentlyContinue
    if ($p) {
        try {
            $candidate = ((& $p.Source -c "import sys;print(sys.executable)") | Select-Object -Last 1).Trim()
            if ($candidate -and (Test-Path $candidate)) { return $candidate }
        } catch {}
    }
    return $null
}

function Ensure-Python {
    $p = Find-Python
    if ($p) { return $p }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Python is missing and winget is unavailable.' }
    & winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw 'Python installation failed.' }
    Refresh-Path
    $p = Find-Python
    if (-not $p) { throw 'Python was installed but could not be located. Reopen PowerShell and run setup again.' }
    return $p
}

Write-Host '[1/7] Checking GitHub CLI and Python...'
$gh = Ensure-Gh
$python = Ensure-Python
Set-Content -Encoding UTF8 -Path (Join-Path $root 'python-path.txt') -Value $python

Write-Host '[2/7] Authenticating GitHub locally...'
& $gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
    & $gh auth login --hostname github.com --web --git-protocol https
    if ($LASTEXITCODE -ne 0) { throw 'GitHub login failed.' }
}

Write-Host '[3/7] Installing local browser-control libraries...'
& $python -m pip install --quiet --upgrade selenium cryptography requests
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }

Write-Host '[4/7] Downloading the persistent bridge files...'
Invoke-WebRequest -UseBasicParsing "$rawBase/send_mail.py" -OutFile (Join-Path $root 'send_mail.py')
Invoke-WebRequest -UseBasicParsing "$rawBase/chrome_keeper.ps1" -OutFile (Join-Path $root 'chrome_keeper.ps1')

Write-Host '[5/7] Creating the local encryption key...'
& $python (Join-Path $root 'send_mail.py') --init-key | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Local key generation failed.' }
$public = Join-Path $root 'public.pem'
if (-not (Test-Path $public)) { throw 'Public key generation failed.' }
$publicB64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($public))
$apiPath = "repos/$repo/contents/.bridge/local/public.pem"
$existingSha = $null
$shaOutput = & $gh api "${apiPath}?ref=$branch" --jq '.sha' 2>$null
if ($LASTEXITCODE -eq 0 -and $shaOutput) { $existingSha = ($shaOutput | Select-Object -Last 1).Trim() }
$args = @('api', '--method', 'PUT', $apiPath, '-f', 'message=Register persistent Naver bridge public key', '-f', "content=$publicB64", '-f', "branch=$branch")
if ($existingSha) { $args += @('-f', "sha=$existingSha") }
& $gh @args | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Uploading the public key to GitHub failed.' }

Write-Host '[6/7] Installing the self-hosted GitHub runner...'
if (-not (Test-Path (Join-Path $runnerDir '.runner'))) {
    $release = Invoke-RestMethod -Headers @{ 'User-Agent' = 'NaverMailBridge' } 'https://api.github.com/repos/actions/runner/releases/latest'
    $asset = $release.assets | Where-Object { $_.name -match '^actions-runner-win-x64-.*\.zip$' } | Select-Object -First 1
    if (-not $asset) { throw 'Could not locate the Windows x64 GitHub Actions runner package.' }
    $zip = Join-Path $root 'actions-runner.zip'
    Invoke-WebRequest -UseBasicParsing $asset.browser_download_url -OutFile $zip
    Get-ChildItem $runnerDir -Force | Remove-Item -Force -Recurse
    Expand-Archive -Force $zip $runnerDir
    Remove-Item $zip -Force
    $registrationOutput = & $gh api --method POST "repos/$repo/actions/runners/registration-token" --jq '.token'
    if ($LASTEXITCODE -ne 0 -or -not $registrationOutput) { throw 'Could not obtain a self-hosted runner registration token.' }
    $registration = ($registrationOutput | Select-Object -Last 1).Trim()
    Push-Location $runnerDir
    try {
        & .\config.cmd --unattended --url "https://github.com/$repo" --token $registration --name "naver-mail-$env:COMPUTERNAME" --labels 'naver-mail' --work '_work' --replace
        if ($LASTEXITCODE -ne 0) { throw 'GitHub runner registration failed.' }
    } finally {
        Pop-Location
    }
}

$runnerKeeper = Join-Path $root 'runner_keeper.ps1'
$runnerKeeperText = @'
$ErrorActionPreference = 'Continue'
$mutex = New-Object System.Threading.Mutex($false, 'Local\NaverMailBridgeRunnerKeeper')
if (-not $mutex.WaitOne(0, $false)) { exit 0 }
Set-Location -LiteralPath "__RUNNER__"
try {
    while ($true) {
        try { & '.\run.cmd' } catch {}
        Start-Sleep -Seconds 10
    }
} finally {
    try { $mutex.ReleaseMutex() } catch {}
    $mutex.Dispose()
}
'@
$runnerKeeperText = $runnerKeeperText.Replace('__RUNNER__', $runnerDir)
Set-Content -Encoding UTF8 -Path $runnerKeeper -Value $runnerKeeperText

$chromeKeeper = Join-Path $root 'chrome_keeper.ps1'
$chromeStartup = Join-Path $startup 'NaverMailPersistentChrome.cmd'
$runnerStartup = Join-Path $startup 'NaverMailGitHubRunner.cmd'
$chromeCmd = @"
@echo off
start "" powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "$chromeKeeper"
"@
$runnerCmd = @"
@echo off
start "" powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "$runnerKeeper"
"@
Set-Content -Encoding ASCII -Path $chromeStartup -Value $chromeCmd
Set-Content -Encoding ASCII -Path $runnerStartup -Value $runnerCmd

Write-Host '[7/7] Starting persistent Chrome and the GitHub runner...'
$chromeArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$chromeKeeper`""
$runnerArgs = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$runnerKeeper`""
Start-Process powershell.exe -WindowStyle Hidden -ArgumentList $chromeArgs
Start-Process powershell.exe -WindowStyle Hidden -ArgumentList $runnerArgs

$deadline = (Get-Date).AddSeconds(45)
$chromeReady = $false
while ((Get-Date) -lt $deadline) {
    try {
        $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:9222/json/version'
        if ($r.StatusCode -eq 200) { $chromeReady = $true; break }
    } catch {}
    Start-Sleep -Seconds 2
}

Write-Host ''
Write-Host '============================================================'
if ($chromeReady) {
    Write-Host 'Persistent Chrome is running.' -ForegroundColor Green
    Write-Host 'Sign in to Naver Mail once in the Chrome window that opened.'
} else {
    Write-Host 'Chrome keeper was installed, but debug port 9222 is not ready yet.' -ForegroundColor Yellow
    Write-Host 'Check that Google Chrome is installed, then rerun this setup.'
}
Write-Host 'The GitHub runner and Chrome keeper restart automatically at Windows logon.'
Write-Host 'Keep this PC powered on and awake when you want ChatGPT mail control.'
Write-Host 'After Naver login, return to ChatGPT and say: 로그인했어'
Write-Host '============================================================'
