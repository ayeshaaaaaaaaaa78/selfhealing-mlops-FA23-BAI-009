pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USER = "${DOCKERHUB_CREDENTIALS_USR}"
    }

    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }

        stage('Build and Run') {
            steps {
                sh 'docker build -t sentiment-api:unstable .'
                sh 'docker rm -f sentiment-test || true'
                sh 'docker run -d --init --name sentiment-test -p 5000:5000 sentiment-api:unstable'
                sh 'sleep 120'
            }
        }

        stage('Unit Test') {
            steps {
                sh 'docker run --rm --network host sentiment-api:unstable pytest tests/test_api.py -v'
            }
        }

        stage('UI Test') {
            steps {
                sh 'docker run --rm --network host sentiment-api:unstable pytest tests/test_ui.py -v'
            }
        }

        stage('Build and Push') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker tag sentiment-api:unstable $DOCKERHUB_USER/sentiment-api:unstable'
                sh 'docker push $DOCKERHUB_USER/sentiment-api:unstable'
                sh 'docker tag sentiment-api:unstable $DOCKERHUB_USER/sentiment-api:stable'
                sh 'docker push $DOCKERHUB_USER/sentiment-api:stable'
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f k8s/pvc.yaml'
                sh 'kubectl apply -f k8s/blue-deployment.yaml'
                sh 'kubectl apply -f k8s/green-deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
            }
        }
    }

    post {
        always {
            sh 'docker rm -f sentiment-test || true'
        }
    }
}
