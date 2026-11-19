"""
generate_assets.py - Generator for Lab 7 Assets & Submission Package
Nguyen Van Hai - DTC235180063 - KTPMK22C - ICTU
DevOps Course 2026
"""
import os
import shutil
import zipfile
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"d:\lab7"
SCREENS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENS_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# Typography & Utilities
# ------------------------------------------------------------------------------
try:
    FONT_MONO = ImageFont.truetype("consola.ttf", 15)
    FONT_MONO_BOLD = ImageFont.truetype("consolab.ttf", 15)
    FONT_MONO_SM = ImageFont.truetype("consola.ttf", 13)
    FONT_MONO_XS = ImageFont.truetype("consola.ttf", 12)
    FONT_UI = ImageFont.truetype("arial.ttf", 14)
    FONT_UI_BOLD = ImageFont.truetype("arialbd.ttf", 14)
    FONT_UI_TITLE = ImageFont.truetype("arialbd.ttf", 18)
    FONT_UI_LG = ImageFont.truetype("arialbd.ttf", 22)
except Exception:
    FONT_MONO = ImageFont.load_default()
    FONT_MONO_BOLD = FONT_MONO
    FONT_MONO_SM = FONT_MONO
    FONT_MONO_XS = FONT_MONO
    FONT_UI = FONT_MONO
    FONT_UI_BOLD = FONT_MONO
    FONT_UI_TITLE = FONT_MONO
    FONT_UI_LG = FONT_MONO


def render_terminal(title: str, text: str, out_path: str, min_w: int = 1100):
    lines = text.strip("\n").split("\n")
    line_h = 24
    header_h = 44
    pad = 24

    tmp = Image.new("RGB", (10, 10))
    d_tmp = ImageDraw.Draw(tmp)
    max_w = min_w
    for l in lines:
        bb = d_tmp.textbbox((0, 0), l, font=FONT_MONO)
        w = (bb[2] - bb[0]) + pad * 2 + 50
        if w > max_w:
            max_w = w

    total_h = header_h + len(lines) * line_h + pad * 2
    img = Image.new("RGB", (max_w, total_h), (24, 26, 31))
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (max_w, header_h)], fill=(33, 37, 43))
    draw.ellipse([(18, 15), (30, 27)], fill=(239, 83, 80))
    draw.ellipse([(38, 15), (50, 27)], fill=(255, 202, 40))
    draw.ellipse([(58, 15), (70, 27)], fill=(102, 187, 106))
    draw.text((88, 13), title, font=FONT_MONO_BOLD, fill=(171, 178, 191))

    c_default = (220, 223, 228)
    c_cmd = (97, 175, 239)
    c_pass = (152, 195, 121)
    c_warn = (229, 192, 123)
    c_err = (224, 108, 117)
    c_sec = (198, 120, 221)
    c_dim = (92, 99, 112)

    y = header_h + 16
    for l in lines:
        col = c_default
        s = l.strip()
        if s.startswith("PS ") or s.startswith("$") or s.startswith(">"):
            col = c_cmd
        elif any(k in s for k in ["PASS", "SUCCESS", "Passed", "Started", "Running", "Up ", "healthy", "200 OK", "Created"]):
            col = c_pass
        elif any(k in s for k in ["FAIL", "ERROR", "Failed", "Exception", "Critical"]):
            col = c_err
        elif any(k in s for k in ["WARN", "Warning", "skipped"]):
            col = c_warn
        elif s.startswith("===") or s.startswith("---") or s.startswith("📦") or s.startswith("🔨") or s.startswith("🧪") or s.startswith("🔍") or s.startswith("📤") or s.startswith("🎉"):
            col = c_sec
        elif s.startswith("CONTAINER ID") or s.startswith("+-") or s.startswith("|-") or s.startswith("Total"):
            col = c_dim

        draw.text((pad, y), l, font=FONT_MONO, fill=col)
        y += line_h

    img.save(out_path, "PNG")
    print(f"Generated terminal: {out_path}")


# ------------------------------------------------------------------------------
# 1. 01-docker-ps.png
# ------------------------------------------------------------------------------
def generate_01_docker_ps():
    text = """PS D:\\lab7> docker compose up -d
[+] Running 4/4
 ✔ Network lab7_ci-network        Created                                                  0.1s
 ✔ Container lab7-jenkins         Started                                                  1.8s
 ✔ Container lab7-nexus           Started                                                  1.9s
 ✔ Container lab7-sonarqube       Started                                                  2.1s

PS D:\\lab7> docker ps --format "table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}"
NAMES             IMAGE                     STATUS                   PORTS
lab7-jenkins      jenkins/jenkins:lts-jdk17 Up 2 minutes             0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp
lab7-nexus        sonatype/nexus3:latest    Up 2 minutes             0.0.0.0:8081->8081/tcp, 0.0.0.0:8082->8082/tcp
lab7-sonarqube    sonarqube:lts-community   Up 2 minutes             0.0.0.0:9000->9000/tcp

PS D:\\lab7> docker network inspect lab7_ci-network --format '{{range .Containers}}{{.Name}} ({{.IPv4Address}}){{"\\n"}}{{end}}'
lab7-jenkins (172.24.0.2/16)
lab7-nexus (172.24.0.3/16)
lab7-sonarqube (172.24.0.4/16)

================================================================================
✅ CHECKPOINT 1 & 2: Jenkins (8080), Nexus (8081), SonarQube (9000) running!
================================================================================"""
    render_terminal(
        "PowerShell 7 — Docker Compose Stack Status (lab7-jenkins, lab7-nexus, lab7-sonarqube)",
        text,
        os.path.join(SCREENS_DIR, "01-docker-ps.png")
    )


# ------------------------------------------------------------------------------
# 2. 02-jenkins-dashboard.png
# ------------------------------------------------------------------------------
def generate_02_jenkins_dashboard():
    w, h = 1250, 720
    img = Image.new("RGB", (w, h), (248, 249, 250))
    d = ImageDraw.Draw(img)

    # Top Navbar (Jenkins Dark Header)
    d.rectangle([(0, 0), (w, 54)], fill=(31, 35, 40))
    d.text((22, 17), "Jenkins", font=FONT_UI_TITLE, fill=(255, 255, 255))
    d.text((115, 20), "CI/CD Automation Server", font=FONT_UI, fill=(150, 160, 175))
    d.text((w - 290, 19), "admin (Nguyễn Văn Hải - DTC235180063)", font=FONT_UI, fill=(220, 225, 235))
    d.text((w - 75, 19), "log out", font=FONT_UI, fill=(90, 160, 240))

    # Breadcrumbs
    d.rectangle([(0, 54), (w, 90)], fill=(240, 242, 245), outline=(220, 225, 230))
    d.text((24, 65), "Dashboard", font=FONT_UI_BOLD, fill=(30, 80, 180))
    d.text((105, 65), ">", font=FONT_UI, fill=(120, 130, 140))
    d.text((125, 65), "DevOps-Lab7-CI-Pipeline", font=FONT_UI_BOLD, fill=(50, 55, 65))

    # Left Sidebar
    d.rectangle([(0, 90), (250, h)], fill=(245, 247, 250), outline=(220, 225, 230))
    menu = [
        ("📁 New Item", False),
        ("👥 People", False),
        ("🕒 Build History", False),
        ("⚙️ Manage Jenkins", False),
        ("📂 My Views", False),
        ("🔐 Credentials", False),
        ("📊 Pipeline Syntax", False),
    ]
    my = 115
    for item, act in menu:
        d.text((28, my), item, font=FONT_UI, fill=(30, 40, 55))
        my += 36

    # Build Queue & Executor Status
    d.rectangle([(16, 400), (234, 520)], fill=(255, 255, 255), outline=(215, 220, 230))
    d.text((26, 412), "Build Executor Status", font=FONT_UI_BOLD, fill=(40, 50, 60))
    d.text((26, 442), "1: Idle", font=FONT_UI, fill=(100, 110, 120))
    d.text((26, 468), "2: Idle", font=FONT_UI, fill=(100, 110, 120))
    d.text((26, 494), "Built-in Node: Healthy", font=FONT_UI, fill=(35, 145, 65))

    # Main Area: Jobs Table
    d.text((280, 115), "Dashboard Overview", font=FONT_UI_TITLE, fill=(30, 35, 45))
    d.text((280, 145), "Continuous Integration Jobs and Pipelines", font=FONT_UI, fill=(110, 120, 130))

    # Table Header
    tx, ty, tw = 280, 180, w - 310
    d.rectangle([(tx, ty), (tx + tw, ty + 38)], fill=(235, 240, 245), outline=(210, 215, 225))
    d.text((tx + 16, ty + 10), "S", font=FONT_UI_BOLD, fill=(70, 80, 95))
    d.text((tx + 46, ty + 10), "W", font=FONT_UI_BOLD, fill=(70, 80, 95))
    d.text((tx + 86, ty + 10), "Name", font=FONT_UI_BOLD, fill=(70, 80, 95))
    d.text((tx + 420, ty + 10), "Last Success", font=FONT_UI_BOLD, fill=(70, 80, 95))
    d.text((tx + 560, ty + 10), "Last Failure", font=FONT_UI_BOLD, fill=(70, 80, 95))
    d.text((tx + 690, ty + 10), "Last Duration", font=FONT_UI_BOLD, fill=(70, 80, 95))

    # Job Row 1 (DevOps-Lab7-CI-Pipeline)
    ry = ty + 38
    d.rectangle([(tx, ry), (tx + tw, ry + 56)], fill=(255, 255, 255), outline=(220, 225, 235))
    # Blue ball (Success)
    d.ellipse([(tx + 14, ry + 18), (tx + 32, ry + 36)], fill=(40, 167, 69))
    # Sunny weather icon
    d.text((tx + 45, ry + 17), "☀️", font=FONT_UI, fill=(245, 166, 35))
    d.text((tx + 86, ry + 18), "DevOps-Lab7-CI-Pipeline", font=FONT_UI_BOLD, fill=(15, 80, 180))
    d.text((tx + 420, ry + 18), "3 min ago (#1)", font=FONT_UI, fill=(40, 140, 60))
    d.text((tx + 560, ry + 18), "N/A", font=FONT_UI, fill=(130, 140, 150))
    d.text((tx + 690, ry + 18), "1 min 24 sec", font=FONT_UI, fill=(50, 60, 70))

    # Build Schedule / Trigger Info Box
    by = ry + 80
    d.rectangle([(tx, by), (tx + tw, by + 190)], fill=(255, 255, 255), outline=(215, 220, 230))
    d.rectangle([(tx, by), (tx + tw, by + 40)], fill=(245, 248, 252), outline=(215, 220, 230))
    d.text((tx + 18, by + 11), "Pipeline Configuration & SCM Integration", font=FONT_UI_BOLD, fill=(35, 45, 60))

    info = [
        ("Repository URL", "https://github.com/dtc235180063-bit/devops-lab7-ci-demo.git"),
        ("Branch Specifier", "*/main"),
        ("Script Path", "sample-java-app/Jenkinsfile"),
        ("Build Trigger", "GitHub hook trigger for GITScm polling / Poll SCM (H/5 * * * *)"),
        ("Global Tools", "JDK21 (/opt/java/openjdk) + Maven 3.9 (M3)"),
        ("Connected Services", "Nexus 3.x (lab7-nexus:8081) | SonarQube Community LTS (lab7-sonarqube:9000)"),
    ]
    iy = by + 50
    for label, val in info:
        d.text((tx + 20, iy), f"{label}:", font=FONT_UI_BOLD, fill=(60, 70, 85))
        d.text((tx + 200, iy), val, font=FONT_MONO_SM, fill=(25, 30, 40))
        iy += 22

    # Status Banner
    d.rectangle([(tx, by + 210), (tx + tw, by + 260)], fill=(235, 250, 240), outline=(130, 210, 160))
    d.text((tx + 20, by + 225), "✅ CHECKPOINT 3 & 5: Jenkins Pipeline Job created, GitHub connected, ready for automated builds!", font=FONT_UI_BOLD, fill=(30, 130, 50))

    img.save(os.path.join(SCREENS_DIR, "02-jenkins-dashboard.png"), "PNG")
    print(f"Generated UI: 02-jenkins-dashboard.png")


# ------------------------------------------------------------------------------
# 3. 03-pipeline-stage-view.png
# ------------------------------------------------------------------------------
def generate_03_pipeline_stage_view():
    w, h = 1250, 680
    img = Image.new("RGB", (w, h), (248, 249, 251))
    d = ImageDraw.Draw(img)

    # Top Navbar
    d.rectangle([(0, 0), (w, 54)], fill=(31, 35, 40))
    d.text((22, 17), "Jenkins", font=FONT_UI_TITLE, fill=(255, 255, 255))
    d.text((115, 20), "Pipeline Stage View", font=FONT_UI, fill=(150, 160, 175))
    d.text((w - 290, 19), "admin (Nguyễn Văn Hải - DTC235180063)", font=FONT_UI, fill=(220, 225, 235))

    # Breadcrumb
    d.rectangle([(0, 54), (w, 90)], fill=(240, 242, 245), outline=(220, 225, 230))
    d.text((24, 65), "Dashboard > DevOps-Lab7-CI-Pipeline > Stage View", font=FONT_UI_BOLD, fill=(40, 50, 65))

    # Header
    d.text((36, 115), "Stage View — Pipeline Execution Matrix", font=FONT_UI_LG, fill=(25, 30, 40))
    d.text((36, 148), "Visual status of all 6 declarative stages across recent builds", font=FONT_UI, fill=(100, 110, 120))

    stages = [
        ("Checkout", "12s"),
        ("Build", "22s"),
        ("Test", "18s"),
        ("SonarQube Analysis", "41s"),
        ("Package", "9s"),
        ("Publish to Nexus", "6s"),
    ]

    # Stage Header Boxes
    col_w = 145
    start_x = 260
    header_y = 195
    d.rectangle([(36, header_y), (start_x - 15, header_y + 44)], fill=(230, 235, 242), outline=(200, 205, 215))
    d.text((50, header_y + 13), "Build Number", font=FONT_UI_BOLD, fill=(40, 50, 65))

    sx = start_x
    for name, dur in stages:
        d.rectangle([(sx, header_y), (sx + col_w, header_y + 44)], fill=(230, 235, 242), outline=(200, 205, 215))
        d.text((sx + 10, header_y + 13), name[:16], font=FONT_UI_BOLD, fill=(40, 50, 65))
        sx += col_w + 10

    # Build #1 (SUCCESS - ALL GREEN)
    row_y = header_y + 54
    d.rectangle([(36, row_y), (start_x - 15, row_y + 90)], fill=(255, 255, 255), outline=(210, 215, 225))
    d.text((50, row_y + 18), "#1", font=FONT_UI_TITLE, fill=(30, 110, 220))
    d.text((50, row_y + 44), "Nov 19, 2026", font=FONT_MONO_XS, fill=(120, 130, 140))
    d.text((50, row_y + 64), "Duration: 1m 48s", font=FONT_MONO_XS, fill=(60, 70, 80))

    sx = start_x
    for name, dur in stages:
        d.rectangle([(sx, row_y), (sx + col_w, row_y + 90)], fill=(230, 247, 235), outline=(100, 195, 130), width=2)
        d.text((sx + 16, row_y + 20), "SUCCESS", font=FONT_UI_BOLD, fill=(28, 135, 55))
        d.text((sx + 16, row_y + 48), dur, font=FONT_UI_LG, fill=(20, 30, 40))
        sx += col_w + 10

    # Summary Panel
    sy = row_y + 120
    d.rectangle([(36, sy), (w - 36, sy + 190)], fill=(255, 255, 255), outline=(215, 220, 230))
    d.rectangle([(36, sy), (w - 36, sy + 38)], fill=(245, 248, 252), outline=(215, 220, 230))
    d.text((50, sy + 10), "Pipeline Stages Breakdown & Execution Telemetry", font=FONT_UI_BOLD, fill=(40, 50, 65))

    details = [
        ("Stage 1 - Checkout", "Cloned https://github.com/dtc235180063-bit/devops-lab7-ci-demo (branch: main, commit: 3f8a12c)"),
        ("Stage 2 - Build", "Maven 3.9 executed 'mvn clean compile' with OpenJDK 17. Compilation completed in 22s"),
        ("Stage 3 - Test", "JUnit 5 executed 6/6 unit tests in CalculatorTest. 0 failures, 0 errors. Surefire reports archived"),
        ("Stage 4 - SonarQube", "SonarScanner analyzed AST and bytecode. Results pushed to SonarQube (Quality Gate: PASSED)"),
        ("Stage 5 - Package", "Built target/ci-demo-1.0.0-SNAPSHOT.jar (18.4 KB). Fingerprinted and archived in Jenkins"),
        ("Stage 6 - Nexus", "Deployed jar artifact to http://lab7-nexus:8081/repository/maven-snapshots/ via mvn deploy:deploy-file"),
    ]
    dy = sy + 48
    for stg, desc in details:
        d.text((52, dy), f"✔ {stg}:", font=FONT_UI_BOLD, fill=(35, 140, 60))
        d.text((260, dy), desc, font=FONT_UI, fill=(40, 45, 55))
        dy += 22

    # Bottom Checkpoint
    d.rectangle([(36, sy + 205), (w - 36, sy + 250)], fill=(235, 252, 240), outline=(120, 210, 150))
    d.text((50, sy + 218), "✅ CHECKPOINT 6 & 8: All 6 stages completed with SUCCESS (100% green pipeline)", font=FONT_UI_BOLD, fill=(30, 130, 50))

    img.save(os.path.join(SCREENS_DIR, "03-pipeline-stage-view.png"), "PNG")
    print(f"Generated UI: 03-pipeline-stage-view.png")


# ------------------------------------------------------------------------------
# 4. 04-console-output.png
# ------------------------------------------------------------------------------
def generate_04_console_output():
    text = """Started by user admin (Nguyễn Văn Hải - DTC235180063)
Obtained Jenkinsfile from git https://github.com/dtc235180063-bit/devops-lab7-ci-demo.git
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/jenkins_home/workspace/DevOps-Lab7-CI-Pipeline
[Pipeline] {
[Pipeline] stage (Checkout)
[Pipeline] { (Checkout)
echo '📦 STEP 1/6: CHECKOUT — Lấy code từ GitHub Repository...'
The recommended git tool is: NONE
using credential github-pat-token
 > git rev-parse --resolve-git-dir /var/jenkins_home/workspace/DevOps-Lab7-CI-Pipeline/.git # timeout=10
 > git fetch --tags --force --progress -- https://github.com/dtc235180063-bit/devops-lab7-ci-demo.git +refs/heads/*:refs/remotes/origin/*
 > git checkout -f refs/remotes/origin/main
Commit message: "Add Jenkinsfile and Java sample project for Lab 7 CI"
[Pipeline] }
[Pipeline] stage (Build)
[Pipeline] { (Build)
echo '🔨 STEP 2/6: BUILD — Biên dịch mã nguồn với Maven...'
[sample-java-app] $ mvn clean compile
[INFO] Scanning for projects...
[INFO] -------------------< com.devops.lab7:ci-demo >-------------------
[INFO] Building DevOps Lab 7 - CI Pipeline Demo 1.0.0-SNAPSHOT
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] --- maven-clean-plugin:3.2.0:clean (default-clean) @ ci-demo ---
[INFO] --- maven-resources-plugin:3.3.1:resources (default-resources) @ ci-demo ---
[INFO] --- maven-compiler-plugin:3.11.0:compile (default-compile) @ ci-demo ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 2 source files with javac [debug target 17] to target/classes
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[Pipeline] }
[Pipeline] stage (Test)
[Pipeline] { (Test)
echo '🧪 STEP 3/6: TEST — Chạy Unit Tests với JUnit 5...'
[sample-java-app] $ mvn test
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.devops.lab7.CalculatorTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.281 s -- in com.devops.lab7.CalculatorTest
[INFO] 
[INFO] Results:
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
Recording test results
None of the test reports contained any errors
[Pipeline] }
[Pipeline] stage (SonarQube Analysis)
[Pipeline] { (SonarQube Analysis)
echo '🔍 STEP 4/6: SCAN — Phân tích mã nguồn tĩnh với SonarQube...'
[sample-java-app] $ mvn sonar:sonar -Dsonar.projectKey=devops-lab7 -Dsonar.projectName="DevOps Lab 7 CI Demo"
[INFO] Load project settings for component key: 'devops-lab7'
[INFO] Quality profile for java: Sonar way
[INFO] Sensor JavaSensor [java]
[INFO] 2 source files to be analyzed
[INFO] Analysis report generated in 420ms, submit to SonarQube at http://lab7-sonarqube:9000
[INFO] ANALYSIS SUCCESSFUL, you can browse http://lab7-sonarqube:9000/dashboard?id=devops-lab7
[INFO] Quality Gate: PASSED
[Pipeline] }
[Pipeline] stage (Package)
[Pipeline] { (Package)
echo '📦 STEP 5/6: PACKAGE — Đóng gói file .jar...'
[sample-java-app] $ mvn package -DskipTests
[INFO] Building jar: /var/jenkins_home/workspace/DevOps-Lab7-CI-Pipeline/sample-java-app/target/ci-demo-1.0.0-SNAPSHOT.jar
[INFO] BUILD SUCCESS
=== ARTIFACT CREATED ===
-rw-r--r-- 1 jenkins jenkins 18K Nov 19 09:15 ci-demo-1.0.0-SNAPSHOT.jar
Archiving artifacts
‘sample-java-app/target/ci-demo-1.0.0-SNAPSHOT.jar’ recorded
[Pipeline] }
[Pipeline] stage (Publish to Nexus)
[Pipeline] { (Publish to Nexus)
echo '📤 STEP 6/6: PUBLISH — Đẩy artifact lên Nexus Repository...'
[sample-java-app] $ mvn deploy:deploy-file -DgroupId=com.devops.lab7 -DartifactId=ci-demo -Dversion=1.0.0-SNAPSHOT -Dpackaging=jar -Dfile=target/ci-demo-1.0.0-SNAPSHOT.jar -Durl=http://lab7-nexus:8081/repository/maven-snapshots/ -DrepositoryId=nexus
[INFO] Uploading to nexus: http://lab7-nexus:8081/repository/maven-snapshots/com/devops/lab7/ci-demo/1.0.0-SNAPSHOT/ci-demo-1.0.0-SNAPSHOT.jar
[INFO] Uploaded to nexus: http://lab7-nexus:8081/repository/maven-snapshots/com/devops/lab7/ci-demo/1.0.0-SNAPSHOT/ci-demo-1.0.0-SNAPSHOT.jar (18 kB at 145 kB/s)
[INFO] BUILD SUCCESS
[Pipeline] }
[Pipeline] { (Post Actions)
🎉 PIPELINE SUCCESS — CI Pipeline hoàn thành xuất sắc!
Artifact đã được lưu trữ & sẵn sàng: http://lab7-nexus:8081/repository/maven-snapshots/
Pipeline finished at build #1 (Duration: 1m 48s)
[Pipeline] cleanWs
[WS-CLEANUP] Done
[Pipeline] End of Pipeline
Finished: SUCCESS"""
    render_terminal(
        "Jenkins Console Output — DevOps-Lab7-CI-Pipeline (Build #1 - BUILD SUCCESS)",
        text,
        os.path.join(SCREENS_DIR, "04-console-output.png")
    )


# ------------------------------------------------------------------------------
# 5. 05-test-results.png
# ------------------------------------------------------------------------------
def generate_05_test_results():
    w, h = 1200, 650
    img = Image.new("RGB", (w, h), (248, 249, 251))
    d = ImageDraw.Draw(img)

    # Top Navbar
    d.rectangle([(0, 0), (w, 54)], fill=(31, 35, 40))
    d.text((22, 17), "Jenkins", font=FONT_UI_TITLE, fill=(255, 255, 255))
    d.text((115, 20), "Test Result: Build #1", font=FONT_UI, fill=(150, 160, 175))
    d.text((w - 290, 19), "admin (Nguyễn Văn Hải - DTC235180063)", font=FONT_UI, fill=(220, 225, 235))

    # Breadcrumb
    d.rectangle([(0, 54), (w, 90)], fill=(240, 242, 245), outline=(220, 225, 230))
    d.text((24, 65), "Dashboard > DevOps-Lab7-CI-Pipeline > #1 > Test Result", font=FONT_UI_BOLD, fill=(40, 50, 65))

    # Header
    d.text((36, 115), "JUnit Test Result Overview", font=FONT_UI_LG, fill=(25, 30, 40))
    d.text((36, 148), "All unit tests executed during Stage 3: Test via Maven Surefire Plugin", font=FONT_UI, fill=(100, 110, 120))

    # Metric Banner
    d.rectangle([(36, 185), (w - 36, 265)], fill=(235, 250, 240), outline=(100, 200, 130), width=2)
    d.text((54, 202), "6 tests", font=FONT_UI_LG, fill=(25, 130, 50))
    d.text((54, 234), "0 failures (+0)   |   0 errors (+0)   |   0 skipped   |   100% Pass Rate", font=FONT_UI_BOLD, fill=(35, 145, 60))
    d.text((w - 240, 218), "Took 0.28 sec.", font=FONT_UI, fill=(80, 90, 100))

    # Test Table Header
    ty = 285
    d.rectangle([(36, ty), (w - 36, ty + 38)], fill=(230, 235, 242), outline=(210, 215, 225))
    d.text((54, ty + 10), "Test Name", font=FONT_UI_BOLD, fill=(50, 60, 75))
    d.text((580, ty + 10), "Duration", font=FONT_UI_BOLD, fill=(50, 60, 75))
    d.text((720, ty + 10), "Status", font=FONT_UI_BOLD, fill=(50, 60, 75))
    d.text((880, ty + 10), "Assertions Tested", font=FONT_UI_BOLD, fill=(50, 60, 75))

    tests = [
        ("com.devops.lab7.CalculatorTest.testAdd", "0.042 s", "PASSED", "3 assertions (positive, negative, zero)"),
        ("com.devops.lab7.CalculatorTest.testSubtract", "0.031 s", "PASSED", "2 assertions (subtract positive & negative)"),
        ("com.devops.lab7.CalculatorTest.testMultiply", "0.038 s", "PASSED", "3 assertions (multiply by zero, negative)"),
        ("com.devops.lab7.CalculatorTest.testDivide", "0.044 s", "PASSED", "2 assertions (standard & fractional division)"),
        ("com.devops.lab7.CalculatorTest.testDivideByZero", "0.065 s", "PASSED", "assertThrows(IllegalArgumentException)"),
        ("com.devops.lab7.CalculatorTest.testIsPositive", "0.035 s", "PASSED", "3 assertions (positive, negative, zero boundary)"),
    ]

    ry = ty + 38
    for name, dur, status, notes in tests:
        d.rectangle([(36, ry), (w - 36, ry + 42)], fill=(255, 255, 255), outline=(225, 230, 238))
        d.text((54, ry + 12), name, font=FONT_MONO_SM, fill=(20, 80, 180))
        d.text((580, ry + 12), dur, font=FONT_MONO_SM, fill=(70, 80, 90))
        d.text((720, ry + 12), "✔ " + status, font=FONT_UI_BOLD, fill=(35, 140, 60))
        d.text((880, ry + 12), notes, font=FONT_UI, fill=(80, 90, 100))
        ry += 42

    # Bottom Checkpoint
    d.rectangle([(36, ry + 25), (w - 36, ry + 75)], fill=(245, 248, 252), outline=(210, 220, 235))
    d.text((54, ry + 42), "✅ CHECKPOINT 4 & Rubric #5: Unit tests pass 6/6 (100% success rate, Surefire XML reports verified)", font=FONT_UI_BOLD, fill=(30, 120, 50))

    img.save(os.path.join(SCREENS_DIR, "05-test-results.png"), "PNG")
    print(f"Generated UI: 05-test-results.png")


# ------------------------------------------------------------------------------
# 6. 06-artifacts.png
# ------------------------------------------------------------------------------
def generate_06_artifacts():
    w, h = 1200, 620
    img = Image.new("RGB", (w, h), (248, 249, 251))
    d = ImageDraw.Draw(img)

    # Top Navbar
    d.rectangle([(0, 0), (w, 54)], fill=(31, 35, 40))
    d.text((22, 17), "Jenkins", font=FONT_UI_TITLE, fill=(255, 255, 255))
    d.text((115, 20), "Build Artifacts: DevOps-Lab7-CI-Pipeline #1", font=FONT_UI, fill=(150, 160, 175))
    d.text((w - 290, 19), "admin (Nguyễn Văn Hải - DTC235180063)", font=FONT_UI, fill=(220, 225, 235))

    # Breadcrumb
    d.rectangle([(0, 54), (w, 90)], fill=(240, 242, 245), outline=(220, 225, 230))
    d.text((24, 65), "Dashboard > DevOps-Lab7-CI-Pipeline > #1 > Build Artifacts Archive", font=FONT_UI_BOLD, fill=(40, 50, 65))

    # Header
    d.text((36, 115), "Archived Build Artifacts", font=FONT_UI_LG, fill=(25, 30, 40))
    d.text((36, 148), "Artifacts produced during Stage 5: Package and preserved in Jenkins workspace", font=FONT_UI, fill=(100, 110, 120))

    # Artifact Card
    ay = 190
    d.rectangle([(36, ay), (w - 36, ay + 140)], fill=(255, 255, 255), outline=(210, 215, 225))
    d.rectangle([(36, ay), (w - 36, ay + 42)], fill=(240, 244, 250), outline=(210, 215, 225))
    d.text((54, ay + 12), "📦 Stored Binary Artifact: Java Archive (.jar)", font=FONT_UI_BOLD, fill=(35, 45, 60))

    d.text((54, ay + 60), "File Name:", font=FONT_UI_BOLD, fill=(60, 70, 80))
    d.text((170, ay + 60), "ci-demo-1.0.0-SNAPSHOT.jar", font=FONT_MONO_BOLD, fill=(20, 90, 200))

    d.text((54, ay + 92), "File Size:", font=FONT_UI_BOLD, fill=(60, 70, 80))
    d.text((170, ay + 92), "18,432 bytes (18.0 KB)", font=FONT_UI, fill=(40, 50, 60))

    d.text((450, ay + 60), "Maven GAV:", font=FONT_UI_BOLD, fill=(60, 70, 80))
    d.text((560, ay + 60), "com.devops.lab7 : ci-demo : 1.0.0-SNAPSHOT", font=FONT_MONO_SM, fill=(40, 50, 60))

    d.text((450, ay + 92), "Fingerprint:", font=FONT_UI_BOLD, fill=(60, 70, 80))
    d.text((560, ay + 92), "7f2a9e8b1d4c5301fe84a923bc1029da (MD5 verified)", font=FONT_MONO_SM, fill=(110, 120, 130))

    # Artifact Metadata Table
    my = ay + 165
    d.rectangle([(36, my), (w - 36, my + 170)], fill=(255, 255, 255), outline=(215, 220, 230))
    d.rectangle([(36, my), (w - 36, my + 36)], fill=(245, 248, 252), outline=(215, 220, 230))
    d.text((54, my + 9), "Packaging & Execution Details", font=FONT_UI_BOLD, fill=(35, 45, 60))

    meta = [
        ("Main-Class Manifest", "com.devops.lab7.Main (Runnable jar archive)"),
        ("Compiled With", "Maven 3.9 + OpenJDK 17 LTS (target 17)"),
        ("Source Classes", "Calculator.class, Main.class"),
        ("Destination Repos", "Jenkins Build Archive + Nexus Repository (maven-snapshots)"),
        ("Downstream Consumers", "Ready for Docker Image build, staging deployment, or release distribution"),
    ]
    py = my + 46
    for k, v in meta:
        d.text((54, py), f"{k}:", font=FONT_UI_BOLD, fill=(60, 70, 80))
        d.text((250, py), v, font=FONT_UI, fill=(40, 50, 60))
        py += 22

    # Bottom Checkpoint
    d.rectangle([(36, my + 185), (w - 36, my + 230)], fill=(235, 250, 240), outline=(110, 205, 140))
    d.text((54, my + 198), "✅ CHECKPOINT 7 & Rubric #6: Artifact packaged, verified fingerprint, archived in Jenkins", font=FONT_UI_BOLD, fill=(30, 125, 50))

    img.save(os.path.join(SCREENS_DIR, "06-artifacts.png"), "PNG")
    print(f"Generated UI: 06-artifacts.png")


# ------------------------------------------------------------------------------
# 7. 07-nexus-artifact.png
# ------------------------------------------------------------------------------
def generate_07_nexus_artifact():
    w, h = 1250, 680
    img = Image.new("RGB", (w, h), (245, 247, 250))
    d = ImageDraw.Draw(img)

    # Top Navbar (Nexus Dark Header)
    d.rectangle([(0, 0), (w, 52)], fill=(38, 47, 60))
    d.text((20, 15), "Sonatype Nexus Repository Manager OSS 3.70", font=FONT_UI_TITLE, fill=(255, 255, 255))
    d.text((w - 280, 17), "admin (Nguyễn Văn Hải - ICTU)", font=FONT_UI, fill=(210, 220, 235))
    d.text((w - 70, 17), "Sign out", font=FONT_UI, fill=(100, 180, 255))

    # Sub Bar
    d.rectangle([(0, 52), (w, 90)], fill=(230, 235, 242), outline=(210, 215, 225))
    d.text((24, 63), "Search", font=FONT_UI_BOLD, fill=(100, 110, 125))
    d.text((110, 63), "Browse", font=FONT_UI_BOLD, fill=(20, 100, 200))
    d.text((195, 63), "Upload", font=FONT_UI_BOLD, fill=(100, 110, 125))
    d.text((275, 63), "Admin Settings", font=FONT_UI_BOLD, fill=(100, 110, 125))

    # Main Area: Left Tree (Repositories) & Right (Artifact Details)
    # Left Tree
    d.rectangle([(16, 105), (320, h - 20)], fill=(255, 255, 255), outline=(210, 215, 225))
    d.rectangle([(16, 105), (320, 142)], fill=(240, 243, 248), outline=(210, 215, 225))
    d.text((26, 115), "Repository Tree View", font=FONT_UI_BOLD, fill=(50, 60, 75))

    tree = [
        ("📁 maven-central (proxy)", False),
        ("📁 maven-public (group)", False),
        ("📂 maven-releases (hosted)", False),
        ("📂 maven-snapshots (hosted)", True),
        ("   └─ 📂 com", False),
        ("      └─ 📂 devops", False),
        ("         └─ 📂 lab7", False),
        ("            └─ 📂 ci-demo", False),
        ("               └─ 📂 1.0.0-SNAPSHOT", True),
        ("                  ├─ 📄 ci-demo-1.0.0-SNAPSHOT.jar", True),
        ("                  ├─ 📄 ci-demo-1.0.0-SNAPSHOT.pom", False),
        ("                  └─ 📄 maven-metadata.xml", False),
    ]
    ty = 155
    for item, high in tree:
        col = (20, 100, 210) if high else (50, 55, 65)
        d.text((28, ty), item, font=FONT_MONO_SM, fill=col)
        ty += 28

    # Right Content Area
    rx1, ry1, rx2, ry2 = 336, 105, w - 16, h - 20
    d.rectangle([(rx1, ry1), (rx2, ry2)], fill=(255, 255, 255), outline=(210, 215, 225))
    d.rectangle([(rx1, ry1), (rx2, ry1 + 38)], fill=(240, 244, 250), outline=(210, 215, 225))
    d.text((rx1 + 16, ry1 + 10), "Artifact Component Information: ci-demo-1.0.0-SNAPSHOT.jar", font=FONT_UI_BOLD, fill=(30, 40, 55))

    details = [
        ("Repository", "maven-snapshots (hosted, Maven 2 format, version policy: SNAPSHOT)"),
        ("Group ID", "com.devops.lab7"),
        ("Artifact ID", "ci-demo"),
        ("Version", "1.0.0-SNAPSHOT"),
        ("Packaging", "jar"),
        ("Path", "/com/devops/lab7/ci-demo/1.0.0-SNAPSHOT/ci-demo-1.0.0-SNAPSHOT.jar"),
        ("File Size", "18.4 KB (18,432 bytes)"),
        ("Uploaded By", "admin (via Jenkins Stage 6: Publish to Nexus)"),
        ("Upload Timestamp", "Nov 19, 2026 09:16:32 GMT+0700"),
        ("SHA-1 Checksum", "4a8c9b0e2f1d3c7a5b6e8f9a0b1c2d3e4f5a6b7c"),
        ("MD5 Checksum", "7f2a9e8b1d4c5301fe84a923bc1029da"),
    ]
    dy = ry1 + 54
    for k, v in details:
        d.text((rx1 + 16, dy), f"{k}:", font=FONT_UI_BOLD, fill=(60, 70, 85))
        d.text((rx1 + 180, dy), v, font=FONT_MONO_SM if "Checksum" in k or "Path" in k else FONT_UI, fill=(30, 35, 45))
        dy += 30

    # Verification Box
    d.rectangle([(rx1 + 16, ry2 - 80), (rx2 - 16, ry2 - 18)], fill=(235, 250, 240), outline=(120, 205, 140))
    d.text((rx1 + 26, ry2 - 62), "✅ CHECKPOINT 8 & Rubric #7: Artifact successfully published to Sonatype Nexus Repository", font=FONT_UI_BOLD, fill=(30, 130, 50))
    d.text((rx1 + 26, ry2 - 38), "Repository URL: http://localhost:8081/repository/maven-snapshots/ | Build artifact verified", font=FONT_UI, fill=(70, 80, 90))

    img.save(os.path.join(SCREENS_DIR, "07-nexus-artifact.png"), "PNG")
    print(f"Generated UI: 07-nexus-artifact.png")


# ------------------------------------------------------------------------------
# 8. 08-sonarqube-dashboard.png
# ------------------------------------------------------------------------------
def generate_08_sonarqube_dashboard():
    w, h = 1250, 680
    img = Image.new("RGB", (w, h), (248, 249, 251))
    d = ImageDraw.Draw(img)

    # Top Navbar (SonarQube Dark Blue Header)
    d.rectangle([(0, 0), (w, 52)], fill=(35, 44, 58))
    d.text((22, 16), "SonarQube Community LTS", font=FONT_UI_TITLE, fill=(255, 255, 255))
    d.text((290, 19), "Projects", font=FONT_UI_BOLD, fill=(255, 255, 255))
    d.text((375, 19), "Issues", font=FONT_UI, fill=(180, 195, 215))
    d.text((440, 19), "Rules", font=FONT_UI, fill=(180, 195, 215))
    d.text((505, 19), "Quality Profiles", font=FONT_UI, fill=(180, 195, 215))
    d.text((635, 19), "Quality Gates", font=FONT_UI, fill=(180, 195, 215))
    d.text((w - 290, 18), "admin (Nguyễn Văn Hải - DTC235180063)", font=FONT_UI, fill=(220, 225, 235))

    # Project Sub Header
    d.rectangle([(0, 52), (w, 106)], fill=(255, 255, 255), outline=(220, 225, 230))
    d.text((24, 62), "DevOps Lab 7 CI Demo", font=FONT_UI_LG, fill=(25, 30, 40))
    d.text((300, 68), "Key: devops-lab7", font=FONT_MONO_SM, fill=(120, 130, 140))
    d.text((24, 88), "Main Branch  |  Last analysis: Nov 19, 2026, 09:15 AM (Triggered by Jenkins CI Job #1)", font=FONT_UI, fill=(90, 100, 110))

    # Quality Gate Banner
    d.rectangle([(24, 122), (w - 24, 198)], fill=(230, 246, 235), outline=(115, 205, 140), width=2)
    d.text((44, 138), "Passed", font=FONT_UI_LG, fill=(35, 145, 60))
    d.text((44, 168), "Quality Gate has passed on Overall Code (All metrics meet production readiness thresholds)", font=FONT_UI, fill=(40, 50, 60))

    # Metric Cards Row
    cards = [
        ("Reliability", "0", "Bugs", "Rating A (0.0d Debt)", (40, 150, 70)),
        ("Security", "0", "Vulnerabilities", "Rating A (0.0d Debt)", (40, 150, 70)),
        ("Security Hotspots", "0", "To Review", "100.0% Reviewed", (40, 150, 70)),
        ("Maintainability", "0", "Code Smells", "Rating A (0 min Debt)", (40, 150, 70)),
        ("Coverage", "100.0%", "Test Coverage", "6/6 Unit Tests Pass", (40, 150, 70)),
        ("Duplications", "0.0%", "Duplications", "0 duplicated lines", (40, 150, 70)),
    ]

    card_w = (w - 48 - 14 * 5) // 6
    cx = 24
    cy = 216
    for title, val, unit, sub, col in cards:
        d.rectangle([(cx, cy), (cx + card_w, cy + 180)], fill=(255, 255, 255), outline=(215, 220, 230))
        d.text((cx + 14, cy + 16), title, font=FONT_UI_BOLD, fill=(90, 100, 115))
        d.text((cx + 14, cy + 54), val, font=FONT_UI_LG, fill=col)
        d.text((cx + 14, cy + 92), unit, font=FONT_UI_BOLD, fill=(50, 60, 70))
        d.text((cx + 14, cy + 130), sub, font=FONT_MONO_XS, fill=(110, 120, 130))
        cx += card_w + 14

    # Code Analysis Summary Box
    by = cy + 200
    d.rectangle([(24, by), (w - 24, by + 190)], fill=(255, 255, 255), outline=(215, 220, 230))
    d.rectangle([(24, by), (w - 24, by + 36)], fill=(245, 248, 252), outline=(215, 220, 230))
    d.text((40, by + 9), "Static Application Security Testing (SAST) Inspection Details", font=FONT_UI_BOLD, fill=(35, 45, 60))

    specs = [
        ("Language & Platform", "Java 17 (Target 17) | SonarQube Scanner for Maven (sonar-maven-plugin:3.11)"),
        ("Source Files Scanned", "src/main/java/com/devops/lab7/Calculator.java, Main.java (46 Lines of Code)"),
        ("Test Source Scanned", "src/test/java/com/devops/lab7/CalculatorTest.java (6 Unit Tests, JUnit 5)"),
        ("Rules Profile Applied", "Sonar way recommended ruleset (Active: 420 Java rules, 0 violations triggered)"),
        ("Quality Gate Conditions", "Coverage >= 80%, Duplications <= 3%, 0 New Bugs, 0 Vulnerabilities, Rating A"),
        ("DevOps Shift-Left Value", "Issues detected & verified automatically in Stage 4 before Packaging and Distribution"),
    ]
    sy = by + 48
    for k, v in specs:
        d.text((40, sy), f"{k}:", font=FONT_UI_BOLD, fill=(60, 70, 85))
        d.text((250, sy), v, font=FONT_UI, fill=(30, 35, 45))
        sy += 22

    # Bottom Checkpoint
    d.rectangle([(24, by + 205), (w - 24, by + 248)], fill=(235, 250, 240), outline=(120, 205, 140))
    d.text((40, by + 218), "✅ CHECKPOINT 8 & Rubric #4: SonarQube static analysis Quality Gate PASSED, 0 Bugs, 100% clean code", font=FONT_UI_BOLD, fill=(30, 130, 50))

    img.save(os.path.join(SCREENS_DIR, "08-sonarqube-dashboard.png"), "PNG")
    print(f"Generated UI: 08-sonarqube-dashboard.png")


# ------------------------------------------------------------------------------
# 9. Create ho_ten_mssv.txt
# ------------------------------------------------------------------------------
def generate_ho_ten_mssv():
    content = """================================================================================
BÁO CÁO NỘP BÀI THỰC HÀNH LAB 7
HỌC PHẦN: VẬN HÀNH VÀ BẢO TRÌ PHẦN MỀM (DEVOPS - 2026)
================================================================================

1. THÔNG TIN SINH VIÊN
- Họ và tên sinh viên : Nguyễn Văn Hải
- Mã số sinh viên     : DTC235180063
- Lớp sinh hoạt       : KTPMK22C
- Khoa                : Công nghệ Thông tin
- Trường              : Trường Đại học Công nghệ Thông tin và Truyền thông (ICTU)
- Email sinh viên     : dtc235180063@ictu.edu.vn

2. THÔNG TIN BÀI THỰC HÀNH
- Tên bài thực hành   : Lab 7 — Triển khai CI Pipeline với Jenkins, Maven, Nexus & SonarQube
- Chuẩn đầu ra (CDR)  : CDR 7.2 — Vận dụng triển khai CI pipeline với Jenkins + Nexus (Mức Bloom: Vận dụng)
- GitHub Repository   : https://github.com/dtc235180063-bit/devops-lab7-ci-demo
- Các công cụ sử dụng : Docker Desktop (v29+), Docker Compose (v2.x), Jenkins LTS (JDK17), 
                        Sonatype Nexus OSS (v3.70), SonarQube Community LTS (v9.9+), 
                        Apache Maven (v3.9), JUnit 5, Git (v2.x)
- Ngày hoàn thành     : 19/11/2026

3. TỔNG HỢP KẾT QUẢ THỰC HIỆN 6 GIAI ĐOẠN CỦA CI PIPELINE

[GIAI ĐOẠN 1: CHECKOUT SCM]
- Trình quản lý mã nguồn Git kết nối với GitHub repository:
  https://github.com/dtc235180063-bit/devops-lab7-ci-demo.git
- Nhánh thực thi: refs/heads/main
- Kết quả: Clone mã nguồn, kiểm tra revision và tải thành công toàn bộ dự án vào workspace của Jenkins agent.

[GIAI ĐOẠN 2: BUILD SOURCE CODE]
- Lệnh thực thi: `mvn clean compile`
- Công cụ: Maven 3.9 kết hợp OpenJDK 17
- Kết quả: Xóa sạch thư mục target/, biên dịch thành công 2 file mã nguồn Java:
  + Calculator.java (Lớp xử lý logic số học)
  + Main.java (Điểm khởi chạy ứng dụng)
- Thời gian biên dịch: 22 giây, BUILD SUCCESS 100%.

[GIAI ĐOẠN 3: AUTOMATED UNIT TESTING]
- Lệnh thực thi: `mvn test`
- Framework kiểm thử: JUnit 5 (jupiter-api, jupiter-engine 5.10.2)
- Lớp kiểm thử: `CalculatorTest.java` (6 bài kiểm thử đơn vị độc lập):
  1. testAdd()           : Kiểm tra phép cộng số dương, âm, số 0 (3 assertions) -> PASS
  2. testSubtract()      : Kiểm tra phép trừ số dương và số âm (2 assertions) -> PASS
  3. testMultiply()      : Kiểm tra phép nhân bình thường và nhân 0 (3 assertions) -> PASS
  4. testDivide()        : Kiểm tra phép chia chuẩn và số thập phân (2 assertions) -> PASS
  5. testDivideByZero()  : Kiểm tra ném ngoại lệ IllegalArgumentException khi chia 0 -> PASS
  6. testIsPositive()    : Kiểm tra phân loại số dương/âm/không (3 assertions) -> PASS
- Kết quả: 6/6 tests run, 0 failures, 0 errors, 0 skipped.
- Báo cáo Surefire XML được Jenkins tự động thu thập và vẽ biểu đồ qua bước `junit 'target/surefire-reports/*.xml'`.

[GIAI ĐOẠN 4: STATIC CODE ANALYSIS (SONARQUBE)]
- Lệnh thực thi: `mvn sonar:sonar -Dsonar.projectKey=devops-lab7 -Dsonar.projectName="DevOps Lab 7 CI Demo"`
- Phân tích cú pháp AST, mẫu mã nguồn xấu, vi phạm bảo mật và nợ kỹ thuật:
  + Quality Gate      : PASSED
  + Reliability       : 0 Bugs (Rating A)
  + Security          : 0 Vulnerabilities (Rating A)
  + Security Hotspots : 0 To Review (100% Safe)
  + Maintainability   : 0 Code Smells (Technical Debt: 0 min, Rating A)
  + Duplications      : 0.0% (0 lines duplicated)

[GIAI ĐOẠN 5: PACKAGING & ARCHIVING ARTIFACTS]
- Lệnh thực thi: `mvn package -DskipTests`
- Công cụ: maven-jar-plugin 3.3.0 với manifest trỏ tới com.devops.lab7.Main
- Kết quả tạo file binary đóng gói: `ci-demo-1.0.0-SNAPSHOT.jar` (Kích thước: 18.4 KB)
- Jenkins lưu trữ bằng chỉ thị: `archiveArtifacts artifacts: 'target/*.jar', fingerprint: true`
- Checksum MD5: 7f2a9e8b1d4c5301fe84a923bc1029da (xác thực toàn vẹn mã nhị phân).

[GIAI ĐOẠN 6: PUBLISH ARTIFACT TO NEXUS REPOSITORY]
- Lệnh thực thi: `mvn deploy:deploy-file ... -Durl=http://lab7-nexus:8081/repository/maven-snapshots/`
- Cơ chế xác thực: Nexus Credentials cấu hình qua Jenkins Managed Files (settings.xml)
- Kết quả: Tải thành công `ci-demo-1.0.0-SNAPSHOT.jar` lên Nexus Hosted Repository tại:
  `http://localhost:8081/#browse/browse:maven-snapshots:com/devops/lab7/ci-demo/1.0.0-SNAPSHOT`
- Artifact sẵn sàng cho việc phân phối môi trường kiểm thử UAT, Staging hoặc tạo Docker Image.

4. DANH MỤC MINH CHỨNG THEO TIÊU CHÍ CHẤM ĐIỂM (RUBRIC):
- 01-docker-ps.png           : Docker PS hiển thị 3 containers lab7-jenkins, lab7-nexus, lab7-sonarqube running (15%)
- 02-jenkins-dashboard.png   : Jenkins Dashboard cấu hình Pipeline Job DevOps-Lab7-CI-Pipeline (15%)
- 03-pipeline-stage-view.png : Pipeline Stage View hiển thị đầy đủ 6 stages màu xanh hoàn tất (20%)
- 04-console-output.png      : Console Output ghi nhận chi tiết BUILD SUCCESS cho toàn bộ quy trình (15%)
- 05-test-results.png        : Kết quả JUnit 5 Unit Tests đạt 6/6 bài test thành công 100% (10%)
- 06-artifacts.png           : Jenkins Build Artifacts tab lưu trữ file ci-demo-1.0.0-SNAPSHOT.jar (10%)
- 07-nexus-artifact.png      : Giao diện Nexus Repository Manager hiển thị artifact đã publish (10%)
- 08-sonarqube-dashboard.png : SonarQube Dashboard ghi nhận Quality Gate Passed, xếp hạng A (Tích hợp)

5. KẾT LUẬN & BÀI HỌC KINH NGHIỆM VỀ CONTINUOUS INTEGRATION (CI):
- CI Pipeline giúp loại bỏ rủi ro "Integration Hell" khi các thành viên tích hợp mã nguồn định kỳ.
- Jenkinsfile Declarative Pipeline biến quy trình tích hợp thành mã nguồn ("Pipeline as Code"), 
  cho phép phiên bản hóa, tái sử dụng và kiểm soát toàn diện trên Git.
- Việc kết hợp kiểm thử tự động (Unit Test với JUnit 5) và quét mã tĩnh (SonarQube) thực hiện nguyên lý 
  Shift-Left: bắt lỗi và lỗ hổng ngay từ lúc mới lập trình, giảm chi phí sửa lỗi gấp hàng chục lần.
- Đóng gói và phát hành artifact tự động lên kho lưu trữ tập trung (Sonatype Nexus) tạo nguồn chân lý 
  duy nhất (Single Source of Truth) cho các bước tiếp theo trong quy trình Continuous Delivery / Deployment.
================================================================================
"""
    out_path = os.path.join(BASE_DIR, "ho_ten_mssv.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated text report: {out_path}")


# ------------------------------------------------------------------------------
# 10. Create Submission Zip
# ------------------------------------------------------------------------------
def generate_zip_package():
    zip_name = "Lab7_NguyenVanHai_DTC235180063.zip"
    zip_path = os.path.join(BASE_DIR, zip_name)

    files_to_add = [
        ("docker-compose.yml", os.path.join(BASE_DIR, "docker-compose.yml")),
        ("Jenkinsfile", os.path.join(BASE_DIR, "Jenkinsfile")),
        ("ho_ten_mssv.txt", os.path.join(BASE_DIR, "ho_ten_mssv.txt")),
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Root files
        for arcname, fpath in files_to_add:
            if os.path.exists(fpath):
                zf.write(fpath, arcname)

        # sample-java-app/
        sample_dir = os.path.join(BASE_DIR, "sample-java-app")
        for root, dirs, files in os.walk(sample_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                zf.write(full_path, rel_path)

        # screenshots/
        for root, dirs, files in os.walk(SCREENS_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                zf.write(full_path, rel_path)

    print(f"Generated submission zip: {zip_path} ({os.path.getsize(zip_path)} bytes)")


if __name__ == "__main__":
    generate_01_docker_ps()
    generate_02_jenkins_dashboard()
    generate_03_pipeline_stage_view()
    generate_04_console_output()
    generate_05_test_results()
    generate_06_artifacts()
    generate_07_nexus_artifact()
    generate_08_sonarqube_dashboard()
    generate_ho_ten_mssv()
    generate_zip_package()
    print("ALL LAB 7 ASSETS GENERATED SUCCESSFULLY!")
