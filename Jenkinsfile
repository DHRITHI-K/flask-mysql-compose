pipeline {
    agent any

    environment {
        IMAGE_NAME = "dhrithi3108/flask-mysql-app"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/DHRITHI-K/flask-mysql-compose.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:latest .'
                }
            }
        }

        stage('Run Container for Test') {
            steps {
                script {
                    sh 'docker run -d -p 5000:5000 --name test_flask $IMAGE_NAME:latest'
                    sh 'sleep 10'
                    sh 'docker ps'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push $IMAGE_NAME:latest
                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh '''
                        docker stop test_flask || true
                        docker rm test_flask || true
                    '''
                }
            }
        }
    }
}
