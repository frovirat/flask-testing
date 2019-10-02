void setBuildStatus(String message, String state) {
    step([
        $class: "GitHubCommitStatusSetter",
        contextSource: [
            $class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"
        ],
        errorHandlers: [
            [$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]
        ],
        statusResultSource: [ $class: "ConditionalStatusResultSource", 
            results: [[$class: "AnyBuildResult", message: message, state: state]]
        ]
    ]);
}

pipeline {
    agent any
    environment {
        DEPLOY_URL = ''
        GROUP_NAME = 'group1'
        GROUP_PORT = '5001'
        PROJECT_NAME = 'flask-testing'
        PACKAGE_NAME = 'apis'
        LOCAL_BRANCH_NAME = ''
        CURRENT_GIT_COMMIT = ''
        CONTAINER_NAME = ''
        CURRENT_IMAGE_NAME = ''
        PREVIOUS_IMAGE_NAME = ''
        MAIL_LIST = "frovirat.ficosa@gmail.com"
    }
    stages {
        stage('Info') {
            steps {
                echo 'Starting'
                setBuildStatus("Build running...", 'PENDING');
                script {
                    def scmVars = checkout scm
                    LOCAL_BRANCH_NAME = scmVars.GIT_BRANCH
                    CURRENT_GIT_COMMIT = scmVars.GIT_COMMIT
                    DEPLOY_URL = BUILD_URL.split('/')[2].split(':')[0]
                    echo DEPLOY_URL
                    echo "Branch Name : " + LOCAL_BRANCH_NAME
                    echo "Commit SHA  : " + CURRENT_GIT_COMMIT
                    CONTAINER_NAME = "testing-flask-$GROUP_NAME"
                    TEMPLATE_IMAGE_NAME = "testing-flask-image-$GROUP_NAME"
                    CURRENT_IMAGE_NAME = "$TEMPLATE_IMAGE_NAME-$CURRENT_GIT_COMMIT"
                    PREVIOUS_IMAGE_NAME = sh (
                        script: "docker ps -f name=$CONTAINER_NAME -q | xargs --no-run-if-empty docker inspect --format='{{.Config.Image}}' $CONTAINER_NAME",
                        returnStdout: true
                    ).trim()
                    echo "Container Name : " + CONTAINER_NAME
                    echo "Current Image Name : " + CURRENT_IMAGE_NAME
                    echo "previous Image Name : $PREVIOUS_IMAGE_NAME"
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
                sh "pip install -r requirements.txt"
                sh "pylint -f parseable --rcfile=.pylintrc $PACKAGE_NAME | tee pylint.out"
                recordIssues(
                    enabledForFailure: true,
                    ignoreFailedBuilds: false,
                    tools: [ pyLint(pattern: 'pylint.out') ],
                    qualityGates: [
                        [threshold: 16, type: 'TOTAL_LOW', unstable: true],
                        [threshold: 11, type: 'TOTAL_NORMAL', unstable: true],
                        [threshold: 1, type: 'TOTAL_HIGH', unstable: true],
                        [threshold: 1, type: 'TOTAL_ERROR', unstable: true]
                    ]
                )
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
                sh "pip install -r requirements.txt"
                sh "py.test --cov -v --junitxml=unittests.xml --cov=$PACKAGE_NAME --cov-config=.coveragerc --cov-report=xml:coverage.xml"
                cobertura(
                    autoUpdateHealth: false,
                    autoUpdateStability: false,
                    coberturaReportFile: '**/coverage.xml',
                    conditionalCoverageTargets: '80, 0, 0',
                    failUnhealthy: false,
                    failUnstable: false,
                    lineCoverageTargets: '80, 0, 0',
                    maxNumberOfBuilds: 0,
                    methodCoverageTargets: '80, 0, 0',
                    onlyStable: false,
                    sourceEncoding: 'ASCII',
                    zoomCoverageChart: false
                )
            }
        }
        stage('Build') {
            when {
                expression { LOCAL_BRANCH_NAME == 'origin/master' }
            }
            steps {
                echo 'Building...'
                sh "docker build -t $CURRENT_IMAGE_NAME ."
            }
        }
        stage('Deploy') {
            when {
                expression { LOCAL_BRANCH_NAME == 'origin/master' }
            }
            steps {
                echo 'Deploying...'
                sh "docker ps -af name=$CONTAINER_NAME -q | xargs --no-run-if-empty docker container rm -f"
                sh "docker run -d -p $GROUP_PORT:5000 --name $CONTAINER_NAME $CURRENT_IMAGE_NAME"
            }
        }
        stage('Health-check') {
            steps {
                sleep 5
                httpRequest(
                        url: "http://$DEPLOY_URL:$GROUP_PORT",
                        validResponseCodes: "200",
                        timeout:30
                    )
            }
        }
    }
    post {
        failure {
                sh "docker image rmi $CURRENT_IMAGE_NAME"
        }
        success {
                sh "docker rmi ${(docker images --format '{{.Repository}}:{{.Tag}}' | grep $PREVIOUS_IMAGE_NAME)}"
        }
        always {
            setBuildStatus("Build results is ${currentBuild.result}", currentBuild.result);
        }
    }
}