
        pipeline {
        agent any

        stages {
            stage('Build') {
                steps {
                    echo 'Building for None ...'
                }
            }
            stage('Test') {
                steps {
                    echo 'Testing for None..'
                }
            }
            stage('Deploy to K8s') {
                steps {
                    echo 'Deploying for None...'
                }
                sh(
                ./kubectl apply -f deployment.yaml
                , returnStatus: false, returnStdout: false)
            }
        }
    }
    