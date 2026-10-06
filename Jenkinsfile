pipeline {
    agent any

    environment {
        IMAGE_NAME = 'sarthi-sanskrit-bot'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code retrieved from GitHub'
            }
        }

        stage('Build') {
            steps {
                dir('backend') {
                    bat 'pip install -r requirements.txt'
                }
                dir('frontend') {
                    bat 'npm install'
                    bat 'npm run build'
                }
            }
        }

        stage('Test / Validate') {
            steps {
                bat 'python -m pytest tests/ -v'
            }
        }

        stage('Docker Build') {
            steps {
                bat "docker build -t %IMAGE_NAME%:%BUILD_NUMBER% ."
                bat "docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest"
            }
        }

        stage('Result') {
            steps {
                bat "docker images %IMAGE_NAME%"
                echo "Build #${env.BUILD_NUMBER} completed successfully"
            }
        }
    }

    post {
        success { echo 'PIPELINE SUCCESS' }
        failure { echo 'PIPELINE FAILED - check console output' }
    }
}
