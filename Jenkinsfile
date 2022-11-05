pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    
    stage('Jenkins Webhook Testing') {
      steps {
              echo 'Auto Push works!' 
      }
    }
    stage('OWASP DependencyCheck') {
      steps {
        dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
      }
    }
  
    stage('SonarQube Testing') {
      steps {
              echo 'Tests' 
      }
    }
    
    stage('Deploy Django') {
      steps {
            sh "docker compose build --pull"
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
