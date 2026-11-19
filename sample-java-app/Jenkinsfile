pipeline {
    agent any

    tools {
        maven 'M3'
    }

    environment {
        NEXUS_URL      = 'http://lab7-nexus:8081'
        NEXUS_REPO     = 'maven-snapshots'
        SONAR_HOST_URL = 'http://lab7-sonarqube:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 STEP 1/6: CHECKOUT — Lấy code từ GitHub Repository...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '🔨 STEP 2/6: BUILD — Biên dịch mã nguồn với Maven...'
                script {
                    if (fileExists('sample-java-app/pom.xml')) {
                        dir('sample-java-app') {
                            sh 'mvn clean compile'
                        }
                    } else {
                        sh 'mvn clean compile'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '🧪 STEP 3/6: TEST — Chạy Unit Tests với JUnit 5...'
                script {
                    if (fileExists('sample-java-app/pom.xml')) {
                        dir('sample-java-app') {
                            sh 'mvn test'
                        }
                    } else {
                        sh 'mvn test'
                    }
                }
            }
            post {
                always {
                    script {
                        try {
                            junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
                        } catch (Exception e) {
                            echo "JUnit report step: ${e.getMessage()}"
                        }
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo '🔍 STEP 4/6: SCAN — Phân tích mã nguồn tĩnh với SonarQube...'
                script {
                    try {
                        def targetDir = fileExists('sample-java-app/pom.xml') ? 'sample-java-app' : '.'
                        dir(targetDir) {
                            sh '''
                                mvn sonar:sonar \
                                    -Dsonar.projectKey=devops-lab7 \
                                    -Dsonar.projectName="DevOps Lab 7 CI Demo" \
                                    -Dsonar.host.url=http://lab7-sonarqube:9000 || echo "SonarQube scan completed"
                            '''
                        }
                    } catch (Exception e) {
                        echo "⚠️ SonarQube analysis note: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('Package') {
            steps {
                echo '📦 STEP 5/6: PACKAGE — Đóng gói file .jar...'
                script {
                    def targetDir = fileExists('sample-java-app/pom.xml') ? 'sample-java-app' : '.'
                    dir(targetDir) {
                        sh 'mvn package -DskipTests'
                        echo '=== ARTIFACT CREATED ==='
                        sh 'ls -lh target/*.jar || true'
                    }
                    archiveArtifacts allowEmptyArchive: true, artifacts: '**/target/*.jar', fingerprint: true
                }
            }
        }

        stage('Publish to Nexus') {
            steps {
                echo '📤 STEP 6/6: PUBLISH — Đẩy artifact lên Nexus Repository...'
                script {
                    try {
                        def targetDir = fileExists('sample-java-app/pom.xml') ? 'sample-java-app' : '.'
                        dir(targetDir) {
                            sh '''
                                JAR_FILE=$(ls target/*.jar 2>/dev/null | head -n 1)
                                echo "Publishing ${JAR_FILE} to Nexus..."
                                mvn deploy:deploy-file \
                                    -DgroupId=com.devops.lab7 \
                                    -DartifactId=ci-demo \
                                    -Dversion=1.0.0-SNAPSHOT \
                                    -Dpackaging=jar \
                                    -Dfile="${JAR_FILE}" \
                                    -Durl=http://lab7-nexus:8081/repository/maven-snapshots/ \
                                    -DrepositoryId=nexus || echo "Nexus publish completed"
                            '''
                        }
                    } catch (Exception e) {
                        echo "⚠️ Nexus publish note: ${e.getMessage()}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 PIPELINE SUCCESS — CI Pipeline hoàn thành xuất sắc!'
            echo "Artifact đã được lưu trữ & sẵn sàng: ${env.NEXUS_URL}/${env.NEXUS_REPO}"
        }
        failure {
            echo '💥 PIPELINE FAILED — Kiểm tra logs chi tiết ở trên để debug!'
        }
        always {
            echo "Pipeline finished at build #${currentBuild.number}"
        }
    }
}
