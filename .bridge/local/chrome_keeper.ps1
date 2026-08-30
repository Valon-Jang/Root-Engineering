$ErrorActionPreference = 'Stop'
$mutex = New-Object System.Threading.Mutex($false, 'Local\NaverMailBridgeChromeKeeper')
if (-not $mutex.WaitOne(0, $false)) { exit 0 }

$root = Join-Path $env:LOCALAPPDATA 'NaverMailBridge'
$profile = Join-Path $root 'profile'
New-Item -ItemType Directory -Force -Path $root, $profile | Out-Null

function Find-Chrome {
    $pf86 = ${env:ProgramFiles(x86)}
    $candidates = @(
        (Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),
        $(if ($pf86) { Join-Path $pf86 'Google\Chrome\Application\chrome.exe' }),
        (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
    ) | Where-Object { $_ }
    foreach ($p in $candidates) { if (Test-Path $p) { return $p } }
    try {
        $reg = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe' -ErrorAction Stop).'(default)'
        if ($reg -and (Test-Path $reg)) { return $reg }
    } catch {}
    throw 'Google Chrome not found.'
}

try {
    $chrome = Find-Chrome
    while ($true) {
        $alive = $false
        try {
            $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:9222/json/version'
            if ($r.StatusCode -eq 200) { $alive = $true }
        } catch {}
        if (-not $alive) {
            $args = @(
                '--remote-debugging-address=127.0.0.1',
                '--remote-debugging-port=9222',
                "--user-data-dir=$profile",
                '--no-first-run',
                '--no-default-browser-check',
                '--window-size=1280,900',
                'https://mail.naver.com'
            )
            Start-Process -FilePath $chrome -ArgumentList $args | Out-Null
        }
        Start-Sleep -Seconds 15
    }
} finally {
    try { $mutex.ReleaseMutex() } catch {}
    $mutex.Dispose()
}
