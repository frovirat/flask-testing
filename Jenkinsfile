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
        GROUP_NAME = 'group1'
        GROUP_PORT = '5001'
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
                echo 'Linting...'
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
                echo 'Testing...'
                //  sh """
                //     py.test --cov -v --junitxml=unittests.xml --cov-config=.coveragerc --cov-report=xml:coverage.xml
                //     """
            }
        }
        stage('Build') {
            // agent { dockerfile true }
            steps {
                echo 'Building...'
                sh "docker build -t flask-testing-image-$GROUP_NAME ."
                echo 'Notify github.'
            }
        }
        stage('Deploy') {
            // agent { dockerfile true }
            steps {
                echo 'Deploying...'
                sh "docker ps -f name=testing-flask-$GROUP_NAME -q | xargs --no-run-if-empty docker container stop"
                sh "docker run -d -p $GROUP_PORT:5000 --name testing-flask-$GROUP_NAME flask-testing-image-$GROUP_NAME"
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
                //sh "docker container ls -a -fname=testing-flask-$GROUP_NAME -q | xargs -r docker container rm"
            }
        }
        stage('fail'){
            steps{
                echo ' que fem en cas de FAIL'
            }
        }
    }
    post {
        always {
            setBuildStatus("Build results is ${currentBuild.result}", currentBuild.result);
        }
    }
}