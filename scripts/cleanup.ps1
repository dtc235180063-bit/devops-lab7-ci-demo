# ============================================================
# cleanup.ps1 — Script dọn dẹp Docker containers Lab 7 (Windows)
# ============================================================
# Usage: .\cleanup.ps1 [-Volumes]

param (
    [switch]$Volumes
)

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  CLEANUP — Lab 7 CI Pipeline Environment" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$baseDir = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path "$baseDir\docker-compose.yml")) {
    $baseDir = $PSScriptRoot
}

Write-Host "Dừng và loại bỏ các containers Lab 7..." -ForegroundColor Yellow
if ($Volumes) {
    Write-Host "⚠️ Đang xóa bỏ containers VÀ data volumes (giải phóng ~3GB)..." -ForegroundColor Red
    docker compose -f "$baseDir\docker-compose.yml" down -v
} else {
    Write-Host "Đang dừng containers (dữ liệu volumes được giữ nguyên)..." -ForegroundColor Green
    docker compose -f "$baseDir\docker-compose.yml" down
}

Write-Host ""
Write-Host "Trạng thái containers sau khi dọn dẹp:" -ForegroundColor Cyan
docker ps -a --filter "name=lab7"
Write-Host ""
Write-Host "Hoàn tất dọn dẹp!" -ForegroundColor Green
