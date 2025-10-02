# GitHub Issues Creation Tool

This directory contains a PowerShell script for creating GitHub issues from CSV files for the MealMind project.

## 🚀 Quick Reference

```powershell
# Preview what will be created (recommended first step)
.\create-github-issues.ps1 -CsvFile ".\phase2-issues.csv" -DryRun

# Create the issues
.\create-github-issues.ps1 -CsvFile ".\phase2-issues.csv"
```

---

## Quick Start

### `create-github-issues.ps1`

A universal script that creates GitHub issues from any CSV file.

#### Usage

```powershell
# Navigate to the planning directory
cd .vscode\planning

# Dry run (preview commands without executing)
.\create-github-issues.ps1 -CsvFile ".\phase1-issues.csv" -DryRun
.\create-github-issues.ps1 -CsvFile ".\phase2-issues.csv" -DryRun

# Create issues for real
.\create-github-issues.ps1 -CsvFile ".\phase1-issues.csv"
.\create-github-issues.ps1 -CsvFile ".\phase2-issues.csv"

# Works with any future phase
.\create-github-issues.ps1 -CsvFile ".\phase3-issues.csv"
```

#### Parameters

- **`-CsvFile`** (Required): Path to the CSV file containing issues
- **`-DryRun`** (Optional): Preview commands without executing them

#### Features

- ✅ Universal - works with any phase CSV file
- ✅ Validates CSV file exists before processing
- ✅ Automatically creates necessary labels with color coding
- ✅ Only creates issues with "Backlog" status
- ✅ Supports all phase labels (phase-1 through phase-6)
- ✅ Shows progress and success/error messages
- ✅ Provides summary count of created issues

#### Supported Labels and Colors

| Label | Color | Hex Code |
|-------|-------|----------|
| phase-1 | Blue | #0075ca |
| phase-2 | Darker Blue | #1d76db |
| phase-3 | Green | #0e8a16 |
| phase-4 | Yellow | #fbca04 |
| phase-5 | Orange | #d93f0b |
| phase-6 | Dark Red | #b60205 |
| setup | Purple | #7057ff |
| backend | Red | #d73a4a |
| frontend | Light Blue | #a2eeef |
| docker | Dark Blue | #0052cc |
| supabase | Green | #00d084 |
| database | Yellow-Orange | #fbca04 |
| python | Yellow | #ffd33d |
| testing | Light Red | #f85149 |

## Project Files

- **`create-github-issues.ps1`** - Universal script for creating GitHub issues
- **`phase1-issues.csv`** - Phase 1: Foundation & Setup (10 issues)
- **`phase2-issues.csv`** - Phase 2: Backend Development (9 issues) ✅ Created
- **`planning.md`** - Complete project planning document
- **`README.md`** - This file

## Already Created Issues

### Phase 2 (Backend Development) ✅
Created on: October 3, 2025

- #48 - Implement Database Schema with Alembic
- #49 - Create Recipe Model and Validation
- #50 - Implement Recipe CRUD Endpoints
- #51 - Implement Meal Plan Model and Validation
- #52 - Implement Meal Planning Endpoints
- #53 - Implement Grocery List Aggregation Logic
- #54 - Implement Grocery List Endpoint
- #55 - Configure CORS for FastAPI
- #56 - Write Comprehensive Backend Tests

View all issues: https://github.com/R4tZz/meal-mind/issues?q=label%3Aphase-2

## CSV File Format

The CSV files use a multi-line format:

```csv
title,body,labels,status
"Issue Title",
"Issue body
with multiple lines
- Acceptance criteria
- More details",
"label1,label2,label3",Backlog
```

### Important Format Rules

1. **Header**: Must be `title,body,labels,status`
2. **Title**: Enclosed in quotes, ends with comma
3. **Body**: Multi-line, enclosed in quotes, ends with comma
4. **Labels**: Comma-separated list in quotes, ends with comma
5. **Status**: Must be "Backlog" for the issue to be created
6. **Record Separator**: Empty line between issues

## Examples

### Create Phase 1 Issues (Dry Run)

```powershell
.\create-github-issues.ps1 -CsvFile ".\phase1-issues.csv" -DryRun
```

Output:
```
🔍 DRY RUN MODE - Commands will be displayed but not executed
📄 CSV File: .\phase1-issues.csv

# Creating labels first:
gh label create 'phase-1' --color '#0075ca' --repo R4tZz/meal-mind
...

# Creating issues:
gh issue create --repo R4tZz/meal-mind --title "Initialize Nx Workspace" ...
```

### Create Phase 2 Issues (Live)

```powershell
.\create-github-issues.ps1 -CsvFile ".\phase2-issues.csv"
```

Output:
```
🚀 LIVE MODE - Issues will be created on GitHub
📄 CSV File: .\phase2-issues.csv

📋 Creating labels first...
✅ Label 'phase-2' created
...

🎫 Creating issues...
✅ Successfully created issue: Implement Database Schema with Alembic
...

========================================
✅ Successfully created 9 issue(s)
========================================
```

## Prerequisites

- PowerShell 5.1 or later
- [GitHub CLI (gh)](https://cli.github.com/) installed and authenticated
- Appropriate repository permissions

## Troubleshooting

### "CSV file not found"

Ensure the path to the CSV file is correct. Use relative or absolute paths.

```powershell
# Relative path
.\create-github-issues.ps1 -CsvFile ".\phase1-issues.csv"

# Absolute path
.\create-github-issues.ps1 -CsvFile "D:\Workspace\meal-mind\.vscode\planning\phase1-issues.csv"
```

### Labels not appearing

The script waits 2 seconds after creating labels. If labels still don't appear, you can manually create them:

```powershell
gh label create "phase-2" --color "#1d76db" --repo R4tZz/meal-mind
```

### Authentication errors

Ensure you're authenticated with GitHub CLI:

```powershell
gh auth status
gh auth login
```

## Contributing

When creating new phase CSV files, follow the existing format and ensure:

1. All issues have "Backlog" status
2. Labels are consistent with the project's labeling scheme
3. Acceptance criteria are clearly defined
4. Issue titles are descriptive and actionable
