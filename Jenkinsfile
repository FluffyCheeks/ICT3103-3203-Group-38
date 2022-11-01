pipeline {
  agent any
  stages {
    stage('OWASP DependencyCheck') {
      steps {
        dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
      }
    }
    stage('Unit Testing') {
      steps {
        sh './pastelLuna/pastelLuna/luna/test.'
      }
    }
  }  
}
  post {
    success {
      dependencyCheckPublisher pattern: 'dependency-check-report.xml'
    }
  }
