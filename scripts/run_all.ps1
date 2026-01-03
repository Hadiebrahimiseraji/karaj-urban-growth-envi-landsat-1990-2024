$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Karaj Urban Growth Analysis Pipeline" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Checking Python 3.8 availability..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($pythonVersion -match '3.8') {
    Write-Host "Python version found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python 3.8 not found in PATH. Using available python..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 1: Validating input data..." -ForegroundColor Cyan
Write-Host ""
python scripts/validate_inputs.py
if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 3) {
    Write-Host "Validation failed. Exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Executing ENVI batch pipeline..." -ForegroundColor Cyan
Write-Host ""
python scripts/envi_batch_pipeline_png.py
$pipelineExitCode = $LASTEXITCODE
if ($pipelineExitCode -eq 3) {
    Write-Host "Warning: ENVI processing not available. Continuing with asset publication..." -ForegroundColor Yellow
} elseif ($pipelineExitCode -ne 0) {
    Write-Host "Pipeline execution failed. Exit code: $pipelineExitCode" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Publishing PNG assets for documentation..." -ForegroundColor Cyan
Write-Host ""
python scripts/publish_assets.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Asset publishing failed. Exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 4: Exporting statistics to CSV..." -ForegroundColor Cyan
Write-Host ""
python scripts/export_stats_csv.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Statistics export failed. Exit code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Pipeline execution completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review validation report: outputs/validation_report.txt" -ForegroundColor White
Write-Host "2. View processing log: outputs/run_log.json" -ForegroundColor White
Write-Host "3. Check statistics: outputs/lulc_stats.csv" -ForegroundColor White
Write-Host "4. Build documentation: mkdocs build" -ForegroundColor White
Write-Host "5. Serve locally: mkdocs serve" -ForegroundColor White
Write-Host ""

exit 0
