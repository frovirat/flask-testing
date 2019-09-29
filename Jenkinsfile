pipeline {
    agent any
    environment {
        PROJECT_NAME = 'flask-testing'
        PACKAGE_NAME = 'apis'
        LOCAL_BRANCH_NAME = ''
        MAIL_LIST = "frovirat.ficosa@gmail.com"
    }
    stages {
        stage('Info') {
            steps {
                echo 'starting'
            }
        }
        stage('Linter') {
            agent {
                docker { 
                    image 'python:3.7'
                }
            }
            steps {
                echo "Installing pylint"
                sh "pip install -U mock pylint"
                echo 'Linting..'
                sh "pylint -f parseable $PACKAGE_NAME | tee pylint.out"
                step([$class: 'WarningsPublisher',
                    parserConfigurations: [
                        [
                        parserName: 'pylint',
                        pattern: 'pylint.out'
                        ]
                    ],
                    unstableTotalLow: '15',
                    unstableTotalNormal: '10',
                    unstableTotalHigh: '0',
                    usePreviousBuildAsReference: true
                ])
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
    post {
        always {
            githubNotify account: 'LopezMDidac', context: 'Final Test',
                credentialsId: '5687d767-8f7e-4647-ad85-f4b842057364', 
                description: 'Notifying to GitHub',
                sha: checkout(scm).GIT_COMMIT,
                status: 'SUCCESS', targetUrl: 'git@github.com:LopezMDidac/flask-testing.git'
        }
    }
}