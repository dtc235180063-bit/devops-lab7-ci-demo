# ============================================================
# verify.ps1 — Script kiểm tra kết quả Lab 7 (Windows PowerShell)
# ============================================================
# Usage: .\verify.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  VERIFY — Lab 7 CI Pipeline Check" -ForegroundColor Cyan
Write-Host "  Sinh viên: Nguyễn Văn Hải - MSSV: DTC235180063" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$Pass = 0
$Fail = 0
$Total = 0

function Check-Result($title, $status, $errMsg = "") {
    $script:Total++
    Write-Host -NoNewline "[$script:Total] $title ... "
    if ($status) {
        Write-Host "✅ PASS" -ForegroundColor Green
        $script:Pass++
    } else {
        Write-Host "❌ FAIL: $errMsg" -ForegroundColor Red
        $script:Fail++
    }
}

$baseDir = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path "$baseDir\docker-compose.yml")) {
    $baseDir = $PSScriptRoot
}

# 1. Check docker-compose.yml
$dcExists = Test-Path "$baseDir\docker-compose.yml"
Check-Result "docker-compose.yml exists" $dcExists "File not found"

if ($dcExists) {
    $dcContent = Get-Content "$baseDir\docker-compose.yml" -Raw
    $hasJenkins = $dcContent -match "jenkins"
    $hasNexus = $dcContent -match "nexus"
    $hasSonar = $dcContent -match "sonarqube"
    Check-Result "docker-compose defines 3 services (Jenkins, Nexus, SonarQube)" ($hasJenkins -and $hasNexus -and $hasSonar) "Missing service"
}

# 2. Check Jenkinsfile
$jfExists = Test-Path "$baseDir\Jenkinsfile"
Check-Result "Jenkinsfile exists" $jfExists "File not found"

if ($jfExists) {
    $jfContent = Get-Content "$baseDir\Jenkinsfile" -Raw
    $hasPipeline = $jfContent -match "pipeline\s*\{"
    Check-Result "Jenkinsfile has declarative pipeline block" $hasPipeline "Missing pipeline declaration"

    $hasStages = ($jfContent -match "stage\('Checkout'\)") -and ($jfContent -match "stage\('Build'\)") -and ($jfContent -match "stage\('Test'\)") -and ($jfContent -match "stage\('Package'\)")
    Check-Result "Jenkinsfile has core stages (Checkout, Build, Test, Package)" $hasStages "Missing stages"

    $hasPublish = $jfContent -match "Nexus"
    Check-Result "Jenkinsfile has Publish to Nexus stage" $hasPublish "Missing Nexus stage"
}

# 3. Check sample-java-app
$pomExists = Test-Path "$baseDir\sample-java-app\pom.xml"
Check-Result "sample-java-app\pom.xml exists" $pomExists "File not found"

$calcExists = Test-Path "$baseDir\sample-java-app\src\main\java\com\devops\lab7\Calculator.java"
Check-Result "Calculator.java source file exists" $calcExists "Source file not found"

$testExists = Test-Path "$baseDir\sample-java-app\src\test\java\com\devops\lab7\CalculatorTest.java"
Check-Result "CalculatorTest.java unit test exists" $testExists "Test file not found"

if ($testExists) {
    $testContent = Get-Content "$baseDir\sample-java-app\src\test\java\com\devops\lab7\CalculatorTest.java" -Raw
    $testCount = ([regex]::Matches($testContent, "@Test")).Count
    Check-Result "CalculatorTest has 6 unit tests (@Test count >= 6)" ($testCount -ge 6) "Only found $testCount tests"
}

# 4. Check Rubric Screenshots
$screens = @(
    "01-docker-ps.png",
    "02-jenkins-dashboard.png",
    "03-pipeline-stage-view.png",
    "04-console-output.png",
    "05-test-results.png",
    "06-artifacts.png",
    "07-nexus-artifact.png",
    "08-sonarqube-dashboard.png"
)

$screenDir = "$baseDir\screenshots"
$allScreens = $true
foreach ($s in $screens) {
    if (-not (Test-Path "$screenDir\$s")) {
        $allScreens = $false
        break
    }
}
Check-Result "All 8 Rubric Screenshots exist in screenshots/" $allScreens "Missing screenshot(s)"

# 5. Check submission package
$reportExists = Test-Path "$baseDir\ho_ten_mssv.txt"
Check-Result "ho_ten_mssv.txt report file exists" $reportExists "Report file not found"

$zipExists = Test-Path "$baseDir\Lab7_NguyenVanHai_DTC235180063.zip"
Check-Result "Submission zip package (Lab7_NguyenVanHai_DTC235180063.zip) exists" $zipExists "Zip not found"

# --- Summary ---
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  RESULTS: $Pass/$Total PASS, $Fail FAIL" -ForegroundColor $(if ($Fail -eq 0) { "Green" } else { "Yellow" })
Write-Host "===============================================" -ForegroundColor Cyan

if ($Fail -eq 0) {
    Write-Host ""
    Write-Host "🎉 Tất cả tiêu chí kiểm tra Lab 7 đã ĐẠT (100% PASS)!" -ForegroundColor Green
    Write-Host "Hồ sơ dự án sẵn sàng nộp bài và đẩy lên GitHub." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️ Có $Fail lỗi cần khắc phục." -ForegroundColor Yellow
}
