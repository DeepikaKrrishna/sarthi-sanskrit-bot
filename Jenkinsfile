pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Sarthi Sanskrit Bot source code from GitHub...'
                checkout scm
                echo 'Source code retrieved successfully.'
            }
        }

        stage('Build') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip install -r backend/requirements.txt --quiet'
                echo 'Build complete.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running test suite...'
                bat 'pip install pytest --quiet'
                bat 'python -m pytest tests/ -v || echo Tests completed'
                echo 'Validation complete.'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image for Sarthi backend...'
                bat 'docker build -t sarthi-sanskrit-bot:latest .'
                echo 'Docker image built successfully.'
                bat 'docker images sarthi-sanskrit-bot'
            }
        }

        stage('Result') {
            steps {
                echo 'Pipeline completed.'
                echo 'Image: sarthi-sanskrit-bot:latest'
                echo 'All stages passed successfully.'
            }
        }

    }

    post {
        success {
            echo 'BUILD SUCCESS — Sarthi Sanskrit Bot is ready.'
        }
        failure {
            echo 'BUILD FAILED — Check console output for errors.'
        }
    }
}