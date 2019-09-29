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
        CURRENT_GIT_COMMIT = ''
        CURRENT_CONTAINER_NAME = ''
        CURRENT_IMAGE_NAME = ''
        PREVIOUS_IMAGE_NAME = ''
        PREVIOUS_CONTAINER_NAME = ''
        MAIL_LIST = "frovirat.ficosa@gmail.com"
    }
    parameters {
        choice(
            choices: ['pass' , 'fail'],
            description: '',
            name: 'SELF_CHECK_STATUS')
    }
    stages {
        stage('Info') {
            steps {
                echo 'Starting'
                script {
                    def scmVars = checkout scm
                    LOCAL_BRANCH_NAME = scmVars.GIT_BRANCH
                    CURRENT_GIT_COMMIT = scmVars.GIT_COMMIT
                    echo "Branch Name : " + LOCAL_BRANCH_NAME
                    echo "Commit SHA  : " + CURRENT_GIT_COMMIT
                    TEMPLATE_CONTAINER_NAME = "testing-flask-$GROUP_NAME"
                    CURRENT_CONTAINER_NAME = "$TEMPLATE_CONTAINER_NAME-$CURRENT_GIT_COMMIT"
                    TEMPLATE_IMAGE_NAME = "flask-testing-image-$GROUP_NAME"
                    CURRENT_IMAGE_NAME = "$TEMPLATE_IMAGE_NAME-$CURRENT_GIT_COMMIT"
                    echo "Current Container Name : " + CURRENT_CONTAINER_NAME
                    echo "Current Imge Name : " + CURRENT_IMAGE_NAME
                }
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
                sh "docker build -t $CURRENT_IMAGE_NAME ."
                echo 'Notify github.'
            }
        }
        stage('Deploy') {
            // agent { dockerfile true }
            steps {
                script {
                    env.PREVIOUS_IMAGE_NAME = sh (
                        script: "docker ps --format {{.Image}} -f name=$TEMPLATE_IMAGE_NAME*",
                        returnStdout: true
                    ).trim()
                    env.PREVIOUS_CONTAINER_NAME = sh (
                        script: "docker ps --format {{.Names}} -f name=$TEMPLATE_IMAGE_NAME*",
                        returnStdout: true
                    ).trim()
                }
            
                echo 'Deploying...'
                
                sh "docker ps -f name=$CURRENT_CONTAINER_NAME -q | xargs --no-run-if-empty docker container stop"
                sh "docker run -d -p $GROUP_PORT:5000 --name $CURRENT_CONTAINER_NAME $CURRENT_IMAGE_NAME"
            }
        }
        stage('Health-check') {
            steps {
                echo 'Ensure that the api is up and giving service'
                script {
                    params.SELF_CHECK_STATUS = 'pass'
                }
            }
        }
        stage('RollBack') {
            when {
                expression { params.SELF_CHECK_STATUS == 'pass' }
            }
            steps {
                echo 'wake up the new image if health-check pass'
                sh "docker container rm -name=$PREVIOUS_CONTAINER_NAME"
            }

            when {
                expression { params.SELF_CHECK_STATUS == 'fail' }
            }
            steps {
                echo 'wake up the old image if health-check fails'
                sh "docker image rm -name=$CURRENT_IMAGE_NAME"
                sh "docker run -d -p $GROUP_PORT:5000 --name $PREVIOUS_CONTAINER_NAME $PREVIOUS_IMAGE_NAME"
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