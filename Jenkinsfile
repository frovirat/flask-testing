pipeline {
    agent none

    stages {
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
        stage('Deploy') {
            agent { dockerfile true }
            steps {
                echo 'Deploying..'
                // docker build -t hello-world-image .
                //docker run  -p 5000:5000 -d --name hello-world hello-world-image
            }
        }
    }
}