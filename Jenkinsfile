pipeline {
  agent any
  stages {
    stage('Stopping Previous Build') {
      steps {
         def buildNumber = env.BUILD_NUMBER as int
         if (buildNumber > 1) milestone(buildNumber - 1)
            milestone(buildNumber)
      }
    }
    
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
  
    stage('Unit Testing & Deploy Django') {
      steps {
          catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh "docker stop pastelluna-django-1"
            sh "docker rm pastelluna-django-1"
          }
           catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh "docker stop pastelluna2-django-1"
            sh "docker rm pastelluna2-django-1"
          }
            sh "docker compose -f docker-compose.yml up --build"
      }
    }
  }
  
  post {
    success {
      dependencyCheckPublisher pattern: 'dependency-check-report.xml'
    }
  }
}


