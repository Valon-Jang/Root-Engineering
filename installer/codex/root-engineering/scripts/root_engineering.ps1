#!/usr/bin/env pwsh

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('init', 'validate', 'validate-package', 'self-test')]
    [string]$Command,

    [string]$ProjectRoot,
    [string]$ProjectName,
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:SkillRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$script:TemplateRoot = Join-Path $script:SkillRoot 'assets/templates'
$script:StartMarker = '<!-- ROOT_ENGINEERING_START -->'
$script:EndMarker = '<!-- ROOT_ENGINEERING_END -->'
$script:ResultPrefix = 'ROOT_ENGINEERING_RESULT='
$script:IsWindowsPlatform = [Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT
$script:PathComparison = if ($script:IsWindowsPlatform) {
    [StringComparison]::OrdinalIgnoreCase
} else {
    [StringComparison]::Ordinal
}
$script:Utf8NoBom = New-Object Text.UTF8Encoding($false, $true)
$script:RootFiles = @(
    [pscustomobject]@{ Relative = 'ROOT.md'; Template = 'ROOT.md' },
    [pscustomobject]@{ Relative = 'FOUNDATION.md'; Template = 'FOUNDATION.md' },
    [pscustomobject]@{ Relative = 'CURRENT.md'; Template = 'CURRENT.md' },
    [pscustomobject]@{ Relative = 'LEARNED.md'; Template = 'LEARNED.md' },
    [pscustomobject]@{ Relative = 'HISTORY.md'; Template = 'HISTORY.md' },
    [pscustomobject]@{ Relative = 'nodes/OPERATIONAL_MEMORY.md'; Template = 'OPERATIONAL_MEMORY.md' }
)
$script:ExpectedRoutes = @(
    '.root/FOUNDATION.md',
    '.root/CURRENT.md',
    '.root/LEARNED.md',
    '.root/nodes/OPERATIONAL_MEMORY.md',
    '.root/HISTORY.md'
)

function Test-ReparsePoint {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        return $false
    }
    $item = Get-Item -Force -LiteralPath $LiteralPath
    return [bool]($item.Attributes -band [IO.FileAttributes]::ReparsePoint)
}

function Test-PathInside {
    param(
        [Parameter(Mandatory = $true)][string]$BasePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    $base = [IO.Path]::GetFullPath($BasePath)
    $target = [IO.Path]::GetFullPath($TargetPath)
    if ($target.Equals($base, $script:PathComparison)) {
        return $true
    }
    $separator = [IO.Path]::DirectorySeparatorChar
    if (-not $base.EndsWith([string]$separator, [StringComparison]::Ordinal)) {
        $base += $separator
    }
    return $target.StartsWith($base, $script:PathComparison)
}

function Resolve-ProjectRoot {
    param([Parameter(Mandatory = $true)][string]$RequestedPath)

    if (-not (Test-Path -LiteralPath $RequestedPath -PathType Container)) {
        throw "Project root does not exist or is not a directory: $RequestedPath"
    }
    $resolved = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $RequestedPath).ProviderPath)
    $filesystemRoot = [IO.Path]::GetPathRoot($resolved)
    if ($resolved.TrimEnd('\', '/').Equals($filesystemRoot.TrimEnd('\', '/'), $script:PathComparison)) {
        throw 'Refusing to initialize a filesystem root.'
    }
    return $resolved
}

function Read-Utf8Text {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    $reader = New-Object IO.StreamReader($LiteralPath, $script:Utf8NoBom, $true)
    try {
        return $reader.ReadToEnd()
    } catch {
        throw "Expected UTF-8 text: $LiteralPath"
    } finally {
        $reader.Dispose()
    }
}

function Write-NewUtf8File {
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $parent = Split-Path -Parent $LiteralPath
    if (-not (Test-Path -LiteralPath $parent)) {
        [IO.Directory]::CreateDirectory($parent) | Out-Null
    }
    $stream = New-Object IO.FileStream(
        $LiteralPath,
        [IO.FileMode]::CreateNew,
        [IO.FileAccess]::Write,
        [IO.FileShare]::None
    )
    $writer = New-Object IO.StreamWriter($stream, $script:Utf8NoBom)
    $writer.NewLine = "`n"
    try {
        $writer.Write($Content)
        $writer.Flush()
        $stream.Flush($true)
    } finally {
        $writer.Dispose()
        $stream.Dispose()
    }
}

function Get-ByteHash {
    param([Parameter(Mandatory = $true)][byte[]]$Bytes)

    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        return [Convert]::ToBase64String($sha.ComputeHash($Bytes))
    } finally {
        $sha.Dispose()
    }
}

function Join-ByteArrays {
    param(
        [Parameter(Mandatory = $true)][byte[]]$First,
        [Parameter(Mandatory = $true)][byte[]]$Second
    )

    $combined = New-Object byte[] ($First.Length + $Second.Length)
    [Array]::Copy($First, 0, $combined, 0, $First.Length)
    [Array]::Copy($Second, 0, $combined, $First.Length, $Second.Length)
    return $combined
}

function Get-MarkerCounts {
    param([Parameter(Mandatory = $true)][string]$Text)

    return [pscustomobject]@{
        Start = ([regex]::Matches($Text, [regex]::Escape($script:StartMarker))).Count
        End = ([regex]::Matches($Text, [regex]::Escape($script:EndMarker))).Count
    }
}

function Test-ProjectName {
    param([Parameter(Mandatory = $true)][string]$Name)

    $candidate = $Name.Trim()
    if ([string]::IsNullOrWhiteSpace($candidate)) {
        throw 'Project name must not be empty.'
    }
    if ($candidate.Length -gt 200 -or $candidate -match '[\x00-\x1f]') {
        throw 'Project name contains unsupported control characters or is too long.'
    }
    if ($candidate.Contains('{{') -or $candidate.Contains('}}')) {
        throw 'Project name must not contain template delimiters.'
    }
    return $candidate
}

function Get-RenderedTemplate {
    param(
        [Parameter(Mandatory = $true)][string]$TemplateName,
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Date
    )

    $templatePath = Join-Path $script:TemplateRoot $TemplateName
    if (Test-ReparsePoint -LiteralPath $templatePath) {
        throw "Template must not be a symlink or reparse point: $templatePath"
    }
    $rendered = (Read-Utf8Text -LiteralPath $templatePath).Replace('{{PROJECT_NAME}}', $Name).Replace('{{DATE}}', $Date)
    if ($rendered.Contains('{{') -or $rendered.Contains('}}')) {
        throw "Unresolved template placeholder in $TemplateName"
    }
    return $rendered.TrimEnd() + "`n"
}

function Get-RootValidationErrors {
    param(
        [Parameter(Mandatory = $true)][string]$RootDirectory,
        [Parameter(Mandatory = $true)][string]$ResolvedProjectRoot,
        [switch]$CheckPublishedRoutes
    )

    $errors = New-Object 'System.Collections.Generic.List[string]'
    if (-not (Test-Path -LiteralPath $RootDirectory -PathType Container)) {
        $errors.Add("Missing Root directory: $RootDirectory")
        return $errors
    }
    if (Test-ReparsePoint -LiteralPath $RootDirectory) {
        $errors.Add("Root directory must not be a symlink or reparse point: $RootDirectory")
        return $errors
    }
    $nodesDirectory = Join-Path $RootDirectory 'nodes'
    if (Test-ReparsePoint -LiteralPath $nodesDirectory) {
        $errors.Add("Nodes directory must not be a symlink or reparse point: $nodesDirectory")
    }

    foreach ($entry in $script:RootFiles) {
        $target = Join-Path $RootDirectory $entry.Relative
        if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
            $errors.Add("Missing required Root node: $($entry.Relative)")
            continue
        }
        if (Test-ReparsePoint -LiteralPath $target) {
            $errors.Add("Root node must not be a symlink or reparse point: $($entry.Relative)")
            continue
        }
        try {
            $text = Read-Utf8Text -LiteralPath $target
        } catch {
            $errors.Add($_.Exception.Message)
            continue
        }
        if ($text -notmatch '\A<!-- ROOT_REVISION: [1-9][0-9]* -->\r?\n') {
            $errors.Add("Missing or invalid ROOT_REVISION header: $($entry.Relative)")
        }
        if ($text.Contains('{{') -or $text.Contains('}}')) {
            $errors.Add("Unresolved template placeholder: $($entry.Relative)")
        }
    }

    $rootMap = Join-Path $RootDirectory 'ROOT.md'
    if (Test-Path -LiteralPath $rootMap -PathType Leaf) {
        $rootText = Read-Utf8Text -LiteralPath $rootMap
        foreach ($route in $script:ExpectedRoutes) {
            if (-not $rootText.Contains(('`' + $route + '`'))) {
                $errors.Add("Missing required route in ROOT.md: $route")
                continue
            }
            if ($CheckPublishedRoutes) {
                $routePath = Join-Path $ResolvedProjectRoot $route
                if (-not (Test-Path -LiteralPath $routePath -PathType Leaf)) {
                    $errors.Add("Route target does not exist: $route")
                    continue
                }
                $resolvedRoute = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $routePath).ProviderPath)
                if (-not (Test-PathInside -BasePath $ResolvedProjectRoot -TargetPath $resolvedRoute)) {
                    $errors.Add("Route escapes the project root: $route")
                }
            }
        }
    }
    return $errors
}

function Get-AgentsValidationErrors {
    param([Parameter(Mandatory = $true)][string]$ResolvedProjectRoot)

    $errors = New-Object 'System.Collections.Generic.List[string]'
    $agentsPath = Join-Path $ResolvedProjectRoot 'AGENTS.md'
    if (-not (Test-Path -LiteralPath $agentsPath -PathType Leaf)) {
        $errors.Add('Missing project AGENTS.md connection file.')
        return $errors
    }
    if (Test-ReparsePoint -LiteralPath $agentsPath) {
        $errors.Add('AGENTS.md must not be a symlink or reparse point.')
        return $errors
    }
    try {
        $text = Read-Utf8Text -LiteralPath $agentsPath
    } catch {
        $errors.Add('AGENTS.md must be UTF-8 before Root Engineering can manage its connection block.')
        return $errors
    }
    $counts = Get-MarkerCounts -Text $text
    if ($counts.Start -ne 1 -or $counts.End -ne 1) {
        $errors.Add("AGENTS.md must contain exactly one complete Root Engineering marker pair (found start=$($counts.Start), end=$($counts.End)).")
    }
    return $errors
}

function Test-RootProject {
    param(
        [Parameter(Mandatory = $true)][string]$ResolvedProjectRoot,
        [switch]$RequireAgents
    )

    $rootDirectory = Join-Path $ResolvedProjectRoot '.root'
    $errors = New-Object 'System.Collections.Generic.List[string]'
    foreach ($errorMessage in @(Get-RootValidationErrors -RootDirectory $rootDirectory -ResolvedProjectRoot $ResolvedProjectRoot -CheckPublishedRoutes)) {
        $errors.Add($errorMessage)
    }
    if ($RequireAgents) {
        foreach ($errorMessage in @(Get-AgentsValidationErrors -ResolvedProjectRoot $ResolvedProjectRoot)) {
            $errors.Add($errorMessage)
        }
    }
    if ($errors.Count -gt 0) {
        throw ("Validation failed:`n- " + ($errors -join "`n- "))
    }
    return [pscustomobject]@{
        action = 'validate'
        status = 'PASS'
        project_root = $ResolvedProjectRoot
        root = $rootDirectory
        required_nodes = $script:RootFiles.Count
        agents_connected = [bool]$RequireAgents
    }
}

function Add-AgentsBlock {
    param([Parameter(Mandatory = $true)][string]$ResolvedProjectRoot)

    $agentsPath = Join-Path $ResolvedProjectRoot 'AGENTS.md'
    if (Test-ReparsePoint -LiteralPath $agentsPath) {
        throw 'Refusing to modify a symlinked or reparse-point AGENTS.md.'
    }
    $blockPath = Join-Path $script:TemplateRoot 'AGENTS_BLOCK.md'
    $block = (Read-Utf8Text -LiteralPath $blockPath).Trim()
    if (-not $block.Contains($script:StartMarker) -or -not $block.Contains($script:EndMarker)) {
        throw 'The bundled AGENTS.md block is missing its marker pair.'
    }

    if (-not (Test-Path -LiteralPath $agentsPath)) {
        try {
            Write-NewUtf8File -LiteralPath $agentsPath -Content ($block + "`n")
        } catch [IO.IOException] {
            throw 'AGENTS.md appeared concurrently; inspect it before retrying.'
        }
        return 'CREATED'
    }

    $originalBytes = [IO.File]::ReadAllBytes($agentsPath)
    $originalText = Read-Utf8Text -LiteralPath $agentsPath
    $counts = Get-MarkerCounts -Text $originalText
    if ($counts.Start -eq 1 -and $counts.End -eq 1) {
        return 'ALREADY_PRESENT'
    }
    if ($counts.Start -ne 0 -or $counts.End -ne 0) {
        throw 'Existing AGENTS.md has an incomplete or duplicate Root Engineering marker block; review it manually.'
    }

    $newline = if ($originalText.Contains("`r`n")) { "`r`n" } else { "`n" }
    $separator = if ($originalText.Length -eq 0 -or $originalText.EndsWith($newline + $newline)) {
        ''
    } elseif ($originalText.EndsWith($newline)) {
        $newline
    } else {
        $newline + $newline
    }
    $normalizedBlock = $block.Replace("`r`n", "`n").Replace("`n", $newline)
    $additionBytes = $script:Utf8NoBom.GetBytes($separator + $normalizedBlock + $newline)
    $candidateBytes = Join-ByteArrays -First $originalBytes -Second $additionBytes
    $transactionId = [Guid]::NewGuid().ToString('N')
    $temporaryPath = Join-Path $ResolvedProjectRoot ('.AGENTS.md.root-engineering-' + $transactionId + '.tmp')
    $backupPath = Join-Path $ResolvedProjectRoot ('.AGENTS.md.root-engineering-' + $transactionId + '.bak')
    $replaceSucceeded = $false
    try {
        $stream = New-Object IO.FileStream(
            $temporaryPath,
            [IO.FileMode]::CreateNew,
            [IO.FileAccess]::Write,
            [IO.FileShare]::None
        )
        try {
            $stream.Write($candidateBytes, 0, $candidateBytes.Length)
            $stream.Flush($true)
        } finally {
            $stream.Dispose()
        }
        $currentBytes = [IO.File]::ReadAllBytes($agentsPath)
        if ((Get-ByteHash -Bytes $currentBytes) -ne (Get-ByteHash -Bytes $originalBytes)) {
            throw 'AGENTS.md changed concurrently; no replacement was made.'
        }
        if (Test-ReparsePoint -LiteralPath $agentsPath) {
            throw 'AGENTS.md became a symlink or reparse point; no replacement was made.'
        }
        [IO.File]::Replace($temporaryPath, $agentsPath, $backupPath)
        $replaceSucceeded = $true
    } finally {
        if (Test-Path -LiteralPath $temporaryPath) {
            Remove-Item -Force -LiteralPath $temporaryPath
        }
        if ($replaceSucceeded -and (Test-Path -LiteralPath $backupPath)) {
            Remove-Item -Force -LiteralPath $backupPath
        }
    }
    return 'APPENDED'
}

function Initialize-RootProject {
    param(
        [Parameter(Mandatory = $true)][string]$ResolvedProjectRoot,
        [string]$RequestedName
    )

    $name = if ([string]::IsNullOrWhiteSpace($RequestedName)) {
        Split-Path -Leaf $ResolvedProjectRoot
    } else {
        $RequestedName
    }
    $name = Test-ProjectName -Name $name
    $rootDirectory = Join-Path $ResolvedProjectRoot '.root'
    if (Test-ReparsePoint -LiteralPath $rootDirectory) {
        throw 'Refusing to initialize a symlinked or reparse-point .root target.'
    }

    $rootStatus = 'ALREADY_PRESENT'
    if (Test-Path -LiteralPath $rootDirectory) {
        Test-RootProject -ResolvedProjectRoot $ResolvedProjectRoot | Out-Null
    } else {
        $stage = Join-Path $ResolvedProjectRoot ('.root-stage-' + [Guid]::NewGuid().ToString('N'))
        if (Test-Path -LiteralPath $stage) {
            throw "Unexpected staging path already exists: $stage"
        }
        try {
            [IO.Directory]::CreateDirectory($stage) | Out-Null
            $date = [DateTime]::UtcNow.ToString('yyyy-MM-dd')
            foreach ($entry in $script:RootFiles) {
                $content = Get-RenderedTemplate -TemplateName $entry.Template -Name $name -Date $date
                Write-NewUtf8File -LiteralPath (Join-Path $stage $entry.Relative) -Content $content
            }
            $stageErrors = @(Get-RootValidationErrors -RootDirectory $stage -ResolvedProjectRoot $ResolvedProjectRoot)
            if ($stageErrors.Count -gt 0) {
                throw ("Staged Root validation failed:`n- " + ($stageErrors -join "`n- "))
            }
            try {
                [IO.Directory]::Move($stage, $rootDirectory)
            } catch {
                throw 'Could not publish the staged Root; the target may have appeared concurrently.'
            }
            $rootStatus = 'CREATED'
        } finally {
            if (Test-Path -LiteralPath $stage) {
                $resolvedStage = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $stage).ProviderPath)
                if ((Test-PathInside -BasePath $ResolvedProjectRoot -TargetPath $resolvedStage) -and
                    ([IO.Path]::GetFileName($resolvedStage)).StartsWith('.root-stage-', [StringComparison]::Ordinal)) {
                    Remove-Item -Recurse -Force -LiteralPath $resolvedStage
                }
            }
        }
    }

    $agentsStatus = Add-AgentsBlock -ResolvedProjectRoot $ResolvedProjectRoot
    $result = Test-RootProject -ResolvedProjectRoot $ResolvedProjectRoot -RequireAgents
    $result.action = 'init'
    $result | Add-Member -NotePropertyName root_status -NotePropertyValue $rootStatus
    $result | Add-Member -NotePropertyName agents_status -NotePropertyValue $agentsStatus
    $result | Add-Member -NotePropertyName project_name -NotePropertyValue $name
    return $result
}

function Test-SkillPackage {
    $errors = New-Object 'System.Collections.Generic.List[string]'
    $expectedPaths = @(
        (Join-Path $script:SkillRoot 'SKILL.md'),
        (Join-Path $script:SkillRoot 'agents/openai.yaml'),
        (Join-Path $script:SkillRoot 'references/PROTOCOL.md'),
        $PSCommandPath,
        (Join-Path $script:TemplateRoot 'ROOT.md'),
        (Join-Path $script:TemplateRoot 'FOUNDATION.md'),
        (Join-Path $script:TemplateRoot 'CURRENT.md'),
        (Join-Path $script:TemplateRoot 'LEARNED.md'),
        (Join-Path $script:TemplateRoot 'HISTORY.md'),
        (Join-Path $script:TemplateRoot 'OPERATIONAL_MEMORY.md'),
        (Join-Path $script:TemplateRoot 'AGENTS_BLOCK.md')
    )
    foreach ($path in $expectedPaths) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            $errors.Add("Missing package file: $path")
        }
    }

    $skillPath = Join-Path $script:SkillRoot 'SKILL.md'
    if (Test-Path -LiteralPath $skillPath -PathType Leaf) {
        $skillText = Read-Utf8Text -LiteralPath $skillPath
        $frontmatter = [regex]::Match($skillText, '\A---\r?\n(?<body>.*?)\r?\n---\r?\n', [Text.RegularExpressions.RegexOptions]::Singleline)
        if (-not $frontmatter.Success) {
            $errors.Add('SKILL.md has invalid or missing YAML frontmatter.')
        } else {
            $metadata = @{}
            foreach ($line in ($frontmatter.Groups['body'].Value -split '\r?\n')) {
                $match = [regex]::Match($line, '^(?<key>[^:]+):\s*(?<value>.*)$')
                if (-not $match.Success) {
                    $errors.Add("Unsupported SKILL.md frontmatter line: $line")
                    continue
                }
                $metadata[$match.Groups['key'].Value.Trim()] = $match.Groups['value'].Value.Trim().Trim('"')
            }
            if ($metadata.Keys.Count -ne 2 -or -not $metadata.ContainsKey('name') -or -not $metadata.ContainsKey('description')) {
                $errors.Add('SKILL.md frontmatter must contain only name and description.')
            }
            if ($metadata['name'] -ne 'root-engineering') {
                $errors.Add('SKILL.md name must be root-engineering.')
            }
            if ($metadata['description'].Length -lt 80) {
                $errors.Add('SKILL.md description is too short to define reliable triggers and boundaries.')
            }
        }
        if (($skillText -split '\r?\n').Count -gt 500) {
            $errors.Add('SKILL.md exceeds the 500-line progressive-disclosure limit.')
        }
    }

    $metadataPath = Join-Path $script:SkillRoot 'agents/openai.yaml'
    if (Test-Path -LiteralPath $metadataPath -PathType Leaf) {
        $metadataText = Read-Utf8Text -LiteralPath $metadataPath
        foreach ($fragment in @(
            'display_name: "Root Engineering"',
            'short_description:',
            'default_prompt: "Use $root-engineering',
            'allow_implicit_invocation: true'
        )) {
            if (-not $metadataText.Contains($fragment)) {
                $errors.Add("agents/openai.yaml is missing: $fragment")
            }
        }
    }

    foreach ($entry in $script:RootFiles) {
        $templatePath = Join-Path $script:TemplateRoot $entry.Template
        if ((Test-Path -LiteralPath $templatePath -PathType Leaf) -and
            ((Read-Utf8Text -LiteralPath $templatePath) -notmatch '\A<!-- ROOT_REVISION: [1-9][0-9]* -->\r?\n')) {
            $errors.Add("Template lacks a valid revision header: $($entry.Template)")
        }
    }

    if ($errors.Count -gt 0) {
        throw ("Package validation failed:`n- " + ($errors -join "`n- "))
    }
    return [pscustomobject]@{
        action = 'validate-package'
        status = 'PASS'
        skill = 'root-engineering'
        package_files = $expectedPaths.Count
    }
}

function Invoke-SelfTest {
    Test-SkillPackage | Out-Null
    $assertions = 1
    $temporaryBase = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
    $sandbox = Join-Path $temporaryBase ('root-engineering-' + [Guid]::NewGuid().ToString('N'))
    [IO.Directory]::CreateDirectory($sandbox) | Out-Null
    try {
        $project = Join-Path $sandbox 'example-project'
        [IO.Directory]::CreateDirectory($project) | Out-Null
        $originalAgents = "# Existing instructions`n`n- Preserve this line.`n"
        Write-NewUtf8File -LiteralPath (Join-Path $project 'AGENTS.md') -Content $originalAgents

        $first = Initialize-RootProject -ResolvedProjectRoot $project -RequestedName 'Example Project'
        if ($first.status -ne 'PASS' -or $first.root_status -ne 'CREATED') { throw 'First initialization did not pass.' }
        $assertions++
        $agentsAfterFirst = Read-Utf8Text -LiteralPath (Join-Path $project 'AGENTS.md')
        if (-not $agentsAfterFirst.Contains($originalAgents.Trim())) { throw 'Existing AGENTS.md content was not preserved.' }
        $assertions++
        $markerCounts = Get-MarkerCounts -Text $agentsAfterFirst
        if ($markerCounts.Start -ne 1 -or $markerCounts.End -ne 1) { throw 'AGENTS.md marker pair is not unique.' }
        $assertions++

        $currentPath = Join-Path $project '.root/CURRENT.md'
        [IO.File]::AppendAllText($currentPath, "`nSENTINEL`n", $script:Utf8NoBom)
        $second = Initialize-RootProject -ResolvedProjectRoot $project -RequestedName 'Example Project'
        if ($second.root_status -ne 'ALREADY_PRESENT' -or $second.agents_status -ne 'ALREADY_PRESENT') {
            throw 'Idempotent initialization did not preserve the existing Root and connection block.'
        }
        $assertions++
        if (-not (Read-Utf8Text -LiteralPath $currentPath).Contains('SENTINEL')) { throw 'Existing Root content was overwritten.' }
        $assertions++
        if ((Get-MarkerCounts -Text (Read-Utf8Text -LiteralPath (Join-Path $project 'AGENTS.md'))).Start -ne 1) {
            throw 'Idempotent initialization duplicated the AGENTS.md block.'
        }
        $assertions++
        Test-RootProject -ResolvedProjectRoot $project -RequireAgents | Out-Null
        $assertions++

        $partial = Join-Path $sandbox 'partial-project'
        [IO.Directory]::CreateDirectory((Join-Path $partial '.root')) | Out-Null
        Write-NewUtf8File -LiteralPath (Join-Path $partial '.root/ROOT.md') -Content "<!-- ROOT_REVISION: 1 -->`n"
        $partialFailed = $false
        try {
            Initialize-RootProject -ResolvedProjectRoot $partial -RequestedName 'Partial Project' | Out-Null
        } catch {
            $partialFailed = $true
        }
        if (-not $partialFailed) { throw 'Partial Root should not be overwritten or accepted.' }
        $assertions++
        if (Test-Path -LiteralPath (Join-Path $partial 'AGENTS.md')) { throw 'Partial Root failure unexpectedly wrote AGENTS.md.' }
        $assertions++

        $broken = Join-Path $sandbox 'broken-project'
        [IO.Directory]::CreateDirectory($broken) | Out-Null
        Initialize-RootProject -ResolvedProjectRoot $broken -RequestedName 'Broken Project' | Out-Null
        [IO.File]::WriteAllText((Join-Path $broken '.root/FOUNDATION.md'), "# Broken`n", $script:Utf8NoBom)
        $brokenFailed = $false
        try {
            Test-RootProject -ResolvedProjectRoot $broken -RequireAgents | Out-Null
        } catch {
            $brokenFailed = $true
        }
        if (-not $brokenFailed) { throw 'Invalid revision header should fail validation.' }
        $assertions++
    } finally {
        if (Test-Path -LiteralPath $sandbox) {
            $resolvedSandbox = [IO.Path]::GetFullPath((Resolve-Path -LiteralPath $sandbox).ProviderPath)
            if ((Test-PathInside -BasePath $temporaryBase -TargetPath $resolvedSandbox) -and
                ([IO.Path]::GetFileName($resolvedSandbox)).StartsWith('root-engineering-', [StringComparison]::Ordinal)) {
                Remove-Item -Recurse -Force -LiteralPath $resolvedSandbox
            }
        }
    }
    return [pscustomobject]@{
        action = 'self-test'
        status = 'PASS'
        assertions = $assertions
        temporary_state_removed = $true
    }
}

function Write-Result {
    param(
        [Parameter(Mandatory = $true)][object]$Result,
        [switch]$AsJson
    )

    $encoded = $Result | ConvertTo-Json -Compress -Depth 6
    if ($AsJson) {
        Write-Output $encoded
    } else {
        Write-Output ($script:ResultPrefix + $encoded)
    }
}

try {
    switch ($Command) {
        'init' {
            if ([string]::IsNullOrWhiteSpace($ProjectRoot)) { throw 'init requires -ProjectRoot.' }
            $resolvedProject = Resolve-ProjectRoot -RequestedPath $ProjectRoot
            $result = Initialize-RootProject -ResolvedProjectRoot $resolvedProject -RequestedName $ProjectName
        }
        'validate' {
            if ([string]::IsNullOrWhiteSpace($ProjectRoot)) { throw 'validate requires -ProjectRoot.' }
            $resolvedProject = Resolve-ProjectRoot -RequestedPath $ProjectRoot
            $result = Test-RootProject -ResolvedProjectRoot $resolvedProject -RequireAgents
        }
        'validate-package' {
            $result = Test-SkillPackage
        }
        'self-test' {
            $result = Invoke-SelfTest
        }
    }
    Write-Result -Result $result -AsJson:$Json
    exit 0
} catch {
    Write-Result -Result ([pscustomobject]@{
        action = $Command
        status = 'FAIL'
        error = $_.Exception.Message
    }) -AsJson:$Json
    exit 1
}
