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
  
    stage('Unit Testing & Deploy Django') {
      steps {
          catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
            sh "docker stop pastelluna-django-1"
            sh "docker rm pastelluna-django-1"
          }
            sh "docker compose -f docker-compose.yml up --build"
      }
    }
  }
  
  def abortPreviousRunningBuilds() {
    def previousBuild = currentBuild.getRawBuild().getPreviousBuildInProgress()
    while (previousBuild != null) {
        if (previousBuild.isInProgress()) {
            def executor = previousBuild.getExecutor()
            if (executor != null) {
                echo ">> Aborting older build #${previousBuild.number}"
                executor.interrupt(Result.ABORTED, new CauseOfInterruption.UserInterruption("Aborted by newer build #${currentBuild.number}"))
            }
        }
        previousBuild = previousBuild.getPreviousBuildInProgress()
    }
  }
  post {
    success {
      dependencyCheckPublisher pattern: 'dependency-check-report.xml'
    }
  }
}
