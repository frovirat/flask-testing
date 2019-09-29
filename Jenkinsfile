void setBuildStatus(String message, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/frovirat/flask-testing.git"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
  ]);
}

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
                echo 'Starting'
            }
        }
        stage('Linter') {
            agent {
                docker { 
                    image 'pylint:latest'
                }
            }
            steps {
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
            agent {
                docker { 
                    image 'pytest-cov:latest'
                }
            }
            steps {
                echo 'Testing..'
            }
        }
        stage('Build') {
            // agent { dockerfile true }
            // steps {
            //     echo 'Building..'
            //     sh "docker build -t flask-testing-image ."
            //     echo 'Notify github.'
            // }
        }
        stage('Deploy') {
            // agent { dockerfile true }
            // steps {
            //     echo 'Deploying..'
            //     sh "docker run -d -p 5000:5000 --name testing-flask flask-testing-image"
            // }
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
        success {
            setBuildStatus("Build succeeded", "SUCCESS");
        }
        failure {
            setBuildStatus("Build failed", "FAILURE");
        }
    }
}