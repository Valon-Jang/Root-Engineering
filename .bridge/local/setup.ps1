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

function Ensure-WingetPackage([string]$command, [string]$id) {
    $x = Get-Command $command -ErrorAction SilentlyContinue
    if ($x) { return $x.Source }
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) { throw "$command is missing and winget is unavailable." }
    & winget install --id $id -e --accept-package-agreements --accept-source-agreements
    Refresh-Path
    $x = Get-Command $command -ErrorAction SilentlyContinue
    if (-not $x) { throw "$command installation finished but the executable was not found. Reopen PowerShell and run setup again." }
    return $x.Source
}

Write-Host '[1/7] Checking GitHub CLI and Python...'
$gh = Ensure-WingetPackage 'gh' 'GitHub.cli'
$python = $null
foreach ($c in @('python', 'py')) {
    $x = Get-Command $c -ErrorAction SilentlyContinue
    if ($x) {
        if ($c -eq 'py') {
            try { $candidate = (& $x.Source -3 -c "import sys;print(sys.executable)").Trim(); if ($candidate) { $python = $candidate; break } } catch {}
        } else {
            try { $candidate = (& $x.Source -c "import sys;print(sys.executable)").Trim(); if ($candidate -and (Test-Path $candidate)) { $python = $candidate; break } } catch {}
        }
    }
}
if (-not $python) {
    Ensure-WingetPackage 'python' 'Python.Python.3.12' | Out-Null
    Refresh-Path
    $candidate = (& python -c "import sys;print(sys.executable)").Trim()
    if (-not $candidate) { throw 'Python could not be located.' }
    $python = $candidate
}
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
$public = Join-Path $root 'public.pem'
if (-not (Test-Path $public)) { throw 'Public key generation failed.' }
$publicB64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($public))
$apiPath = "repos/$repo/contents/.bridge/local/public.pem"
$existingSha = $null
try { $existingSha = (& $gh api "$apiPath`?ref=$branch" --jq '.sha' 2>$null).Trim() } catch {}
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
    $registration = (& $gh api --method POST "repos/$repo/actions/runners/registration-token" --jq '.token').Trim()
    if (-not $registration) { throw 'Could not obtain a self-hosted runner registration token.' }
    Push-Location $runnerDir
    try {
        & .\config.cmd --unattended --url "https://github.com/$repo" --token $registration --name "naver-mail-$env:COMPUTERNAME" --labels 'naver-mail' --work '_work' --replace
        if ($LASTEXITCODE -ne 0) { throw 'GitHub runner registration failed.' }
    } finally { Pop-Location }
}

$runnerKeeper = Join-Path $root 'runner_keeper.ps1'
@"
`$ErrorActionPreference = 'Continue'
Set-Location '$runnerDir'
while (`$true) {
    try { & '.\run.cmd' } catch {}
    Start-Sleep -Seconds 10
}
"@ | Set-Content -Encoding UTF8 $runnerKeeper

$chromeStartup = Join-Path $startup 'NaverMailPersistentChrome.cmd'
$runnerStartup = Join-Path $startup 'NaverMailGitHubRunner.cmd'
"@echo off`r`nstart \"\" powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File \"$root\chrome_keeper.ps1\"`r`n" | Set-Content -Encoding ASCII $chromeStartup
"@echo off`r`nstart \"\" powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File \"$runnerKeeper\"`r`n" | Set-Content -Encoding ASCII $runnerStartup

Write-Host '[7/7] Starting persistent Chrome and the GitHub runner...'
Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $root 'chrome_keeper.ps1'))
Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $runnerKeeper)

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
Write-Host 'The GitHub runner and Chrome keeper will restart automatically at Windows logon.'
Write-Host 'After Naver login, return to ChatGPT and say: 로그인했어'
Write-Host '============================================================'
