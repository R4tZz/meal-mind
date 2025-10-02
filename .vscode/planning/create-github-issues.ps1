param(
    [Parameter(Mandatory=$true)]
    [string]$CsvFile,
    
    [switch]$DryRun = $false
)

# Function to create labels if they don't exist
function Ensure-Labels {
    param([string[]]$Labels)
    
    $uniqueLabels = $Labels | Sort-Object -Unique
    
    # Define colors for different label types
    $labelColors = @{
        'phase-1' = '#0075ca'      # Blue
        'phase-2' = '#1d76db'      # Darker Blue
        'phase-3' = '#0e8a16'      # Green
        'phase-4' = '#fbca04'      # Yellow
        'phase-5' = '#d93f0b'      # Orange
        'phase-6' = '#b60205'      # Dark Red
        'setup' = '#7057ff'        # Purple  
        'backend' = '#d73a4a'      # Red
        'frontend' = '#a2eeef'     # Light blue
        'docker' = '#0052cc'       # Dark blue
        'supabase' = '#00d084'     # Green
        'database' = '#fbca04'     # Yellow-orange
        'python' = '#ffd33d'       # Yellow
        'testing' = '#f85149'      # Light red
    }
    
    foreach ($label in $uniqueLabels) {
        if ($DryRun) {
            $color = $labelColors[$label] ?? '#d4d4d8'  # Default gray
            Write-Output "gh label create '$label' --color '$color' --repo R4tZz/meal-mind"
        } else {
            Write-Host "Ensuring label exists: $label" -ForegroundColor Cyan
            try {
                # Check if label already exists first
                $existingLabel = gh label list --repo R4tZz/meal-mind --search $label 2>$null | Where-Object { $_ -match "^$label\s" }
                if ($existingLabel) {
                    Write-Host "ℹ️  Label '$label' already exists" -ForegroundColor Yellow
                } else {
                    # Create the label with proper hex color
                    $color = $labelColors[$label] ?? '#d4d4d8'  # Default gray
                    gh label create $label --color $color --repo R4tZz/meal-mind
                    Write-Host "✅ Label '$label' created" -ForegroundColor Green
                }
            } catch {
                Write-Host "❌ Failed to create label '$label': $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
    
    if (-not $DryRun) { 
        Write-Host ""
        Write-Host "⏳ Waiting 2 seconds for labels to propagate..." -ForegroundColor Cyan
        Start-Sleep -Seconds 2
        Write-Host ""
    }
}

# Validate CSV file exists
if (-not (Test-Path $CsvFile)) {
    Write-Host "❌ Error: CSV file not found: $CsvFile" -ForegroundColor Red
    exit 1
}

# Read the CSV file and parse manually due to non-standard multi-line format
$content = Get-Content $CsvFile -Raw

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - Commands will be displayed but not executed" -ForegroundColor Yellow
    Write-Host "📄 CSV File: $CsvFile" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "🚀 LIVE MODE - Issues will be created on GitHub" -ForegroundColor Green
    Write-Host "📄 CSV File: $CsvFile" -ForegroundColor Green
    Write-Host ""
}

# Remove the header line first
$content = $content -replace "^title,body,labels,status`r?`n", ""

# Split by double newlines to get each record
$records = $content -split "`r?`n`r?`n" | Where-Object { $_.Trim() -ne "" }

# First pass: collect all labels that will be needed
$allLabels = @()
foreach ($record in $records) {
    $lines = $record -split "`r?`n" | Where-Object { $_.Trim() -ne "" }
    
    if ($lines.Count -ge 3) {
        # Last line should be labels and status
        $lastLine = $lines[-1]
        if ($lastLine -match '^"([^"]+)",\s*(.+)\s*$') {
            $labels = $matches[1]
            $status = $matches[2].Trim()
            
            # Only collect labels for issues that will be created (Backlog status)
            if ($status -eq "Backlog") {
                $labelArray = $labels -split ',' | ForEach-Object { $_.Trim() }
                $allLabels += $labelArray
            }
        }
    }
}

# Create all needed labels first
if ($allLabels.Count -gt 0) {
    if ($DryRun) {
        Write-Output "# Creating labels first:"
    } else {
        Write-Host "📋 Creating labels first..." -ForegroundColor Magenta
    }
    Ensure-Labels -Labels $allLabels
}

# Second pass: create the issues
if ($DryRun) {
    Write-Output "# Creating issues:"
} else {
    Write-Host "🎫 Creating issues..." -ForegroundColor Magenta
}

$issueCount = 0
foreach ($record in $records) {
    $lines = $record -split "`r?`n" | Where-Object { $_.Trim() -ne "" }
    
    if ($lines.Count -ge 3) {
        # First line should be the title (in quotes, ending with comma)
        $titleLine = $lines[0]
        if ($titleLine -match '^"([^"]+)",\s*$') {
            $title = $matches[1]
        } else {
            Write-Output "# Could not parse title from: $titleLine"
            continue
        }
        
        # Last line should be labels and status
        $lastLine = $lines[-1]
        if ($lastLine -match '^"([^"]+)",\s*(.+)\s*$') {
            $labels = $matches[1]
            $status = $matches[2].Trim()
        } else {
            Write-Output "# Could not parse labels/status from: $lastLine"
            continue
        }
        
        # Middle lines are the body (remove quotes from first and last body lines)
        $bodyLines = $lines[1..($lines.Count - 2)]
        if ($bodyLines.Count -gt 0) {
            # Remove leading quote from first body line and trailing quote+comma from last body line
            $bodyLines[0] = $bodyLines[0] -replace '^"', ''
            $bodyLines[-1] = $bodyLines[-1] -replace '",\s*$', ''
            $body = $bodyLines -join "`n"
        } else {
            $body = ""
        }
        
        # Only create issues that are in Backlog status
        if ($status -eq "Backlog") {
            $command = "gh issue create --repo R4tZz/meal-mind --title `"$title`" --body `"$body`" --label $labels"
            
            if ($DryRun) {
                Write-Output $command
            } else {
                Write-Host "Creating issue: $title" -ForegroundColor Cyan
                try {
                    $result = Invoke-Expression $command 2>&1
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "✅ Successfully created issue: $title" -ForegroundColor Green
                        $issueCount++
                    } else {
                        Write-Host "❌ Failed to create issue: $title" -ForegroundColor Red
                        Write-Host "Error output: $result" -ForegroundColor Red
                    }
                } catch {
                    Write-Host "❌ Failed to create issue: $title" -ForegroundColor Red
                    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
                }
                Write-Host ""
            }
        } else {
            if ($DryRun) {
                Write-Output "# Skipping '$title' - Status: $status"
            } else {
                Write-Host "⏭️  Skipping '$title' - Status: $status" -ForegroundColor Yellow
            }
        }
    } else {
        if ($DryRun) {
            Write-Output "# Skipping malformed record with $($lines.Count) lines"
        } else {
            Write-Host "⚠️  Skipping malformed record with $($lines.Count) lines" -ForegroundColor Yellow
        }
    }
}

# Summary
if (-not $DryRun -and $issueCount -gt 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Successfully created $issueCount issue(s)" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
}
