pipeline {
  agent any

  environment {
    IMAGE_NAME = "yourdockerhubusername/flask-mysql-app"
    DOCKERHUB_CRED_ID = "dockerhub-creds"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:latest ."
      }
    }

    stage('Test Container') {
      steps {
        sh """
          docker run -d -p 5001:5000 --name test_app ${IMAGE_NAME}:latest
          sleep 5
          curl -f http://localhost:5001 || (echo 'App failed' && exit 1)
          docker stop test_app
          docker rm test_app
        """
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CRED_ID}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh """
            echo $PASS | docker login -u $USER --password-stdin
            docker push ${IMAGE_NAME}:latest
            docker logout
          """
        }
      }
    }
  }
}
