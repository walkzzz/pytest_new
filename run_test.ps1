# Force fix PowerShell Chinese encoding issues
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null

# Clean up all cache and old reports
Remove-Item allure-results -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item allure-report -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Directory -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Cleanup completed" -ForegroundColor Green

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

# Run tests
Write-Host "Running tests..." -ForegroundColor Cyan
python -m pytest tests --alluredir=allure-results

# Generate and open report
Write-Host "Generating Allure report..." -ForegroundColor Cyan
allure generate allure-results -o allure-report --clean
Write-Host "Opening report..." -ForegroundColor Cyan
allure open allure-report