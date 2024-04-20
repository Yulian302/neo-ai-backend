pipeline {
    agent {
    docker {
          // Set both label and image
          label 'docker'
          image 'python:3.12.1-alpine3.19'
          args '--name docker-node' // list any args
        }
    }

    stages {
        stage('init'){
        env.PATH = "${tool 'docker'}/bin:${tool 'maven'}/bin:${env.PATH}"
        }
        stage('build') {

            steps {
                sh 'python --version'
            }
        }
    }
}
