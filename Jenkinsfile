pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('OWASP DependencyCheck') {
      steps {
        dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
      }
    }
  
    stage('Build Docker') {
      steps {
              echo 'Test' 
      }
    }
    stage('Setup Django') {
      steps {
              echo 'Test' 
      }
    }
    
    stage('Unit Testing') {
      steps {
              echo 'Test' 
      }
    }
    
  }
  post {
    success {
      dependencyCheckPublisher pattern: 'dependency-check-report.xml'
    }
  }
}
