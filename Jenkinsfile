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
                echo 'Notify github.'
            }
        }
        stage('Deploy') {
            // agent { dockerfile true }
            steps {
                echo 'Deploying..'
                sh "docker run -d -p 5000:5000 --name testing-flask flask-testing-image"
            }
        }
        stage('Health-check') {
            steps {
                echo 'Ensure that the api is up and giving service'
            }
        }
        stage('RollBack') {
            steps {
                echo 'wake up the old image if health-check fails'
            }
        }
        stage('fail'){
            steps{
                echo ' que fem'
            }
        }
    }
}