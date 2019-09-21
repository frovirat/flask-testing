pipeline {
    agent any

    stages {
        stage('Info') {
            steps {
                echo 'starting'
            }
        }
        stage('Linter') {
            steps {
                echo 'Linting..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Build') {
            // agent { dockerfile true }
            steps {
                echo 'Building..'
                sh "docker build -t flask-testing-image ."
            }
        }
        stage('Deploy') {
            // agent { dockerfile true }
            steps {
                echo 'Deploying..'
                sh "docker run -d -p 5000:5000 --name testing-flask flask-testing-image"
            }
        }
    }
}