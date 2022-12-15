pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "hoangsndxqn/kms-picture-finder-ai-service"
    }
    stages {
        stage('Prepare workspace') {
            steps {
                echo 'Prepare workspace'
                step([$class: 'WsCleanup'])
                script {
                    def commit = checkout scm
                    env.BRANCH_NAME = commit.GIT_BRANCH.replace('origin/', '')
                }
            }
        }
        stage('Docker build and push images') {
            environment {
                DOCKER_TAG="${GIT_BRANCH.tokenize('/').pop()}-${GIT_COMMIT.substring(0,7)}"
            } 
            steps {
                script {
                    echo DOCKER_TAG
                }
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} . "
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                sh "docker image ls | grep ${DOCKER_IMAGE}"
                withDockerRegistry(credentialsId: 'docker-hub', url: 'https://index.docker.io/v1/') {
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
                sh "docker image rm ${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh "docker image rm ${DOCKER_IMAGE}:latest"
            }
        }
        stage('Delpoy: DEVELOP') {
            when {
                expression {
                    return (env.BRANCH_NAME == 'dev')
                }
            }
            steps{
                sh 'echo deploy to server dev'
                sh "ssh -i /var/jenkins_home/.ssh/key_ai_dev hoangsndxqn@34.125.145.141 './developAI.sh'"
            }
        }
        stage('Delpoy: RELEASE') {
            when {
                expression {
                    return (env.BRANCH_NAME == "refs/tags/${GIT_BRANCH.tokenize('/').pop()}")
                }
            }
            steps{
                sh 'echo deploy to SERVER 1'
                sh "ssh -i /var/jenkins_home/.ssh/id_aiserver hoangsndxqn@35.247.172.2 './releaseAI.sh'"
                sh 'echo deploy to SERVER 2'
                sh "ssh -i /var/jenkins_home/.ssh/key_ai1 hoangsndxqn@34.87.94.31 './releaseAI.sh'"
            }
        }
    }
    post {
        success {
            echo "SUCCESSFUL"
        }
        failure {
            echo "FAILED"
        }
    }
}
