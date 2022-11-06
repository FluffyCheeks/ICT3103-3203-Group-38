@NonCPS
def cancelPreviousBuilds() {
    def jobName = env.JOB_NAME
    def buildNumber = env.BUILD_NUMBER.toInteger()

    /* Get job name */
    def currentJob = Jenkins.instance.getItemByFullName(jobName)

    /* Iterating over the builds for specific job */
    for (def build : currentJob.builds) {
        def listener = build.getListener()
        def exec = build.getExecutor()
        /* If there is a build that is currently running and it's not current build */
        if (build.isBuilding() && build.number.toInteger() < buildNumber && exec != null) {
            /* Then stop it */
            exec.interrupt(
                    Result.ABORTED,
                    new CauseOfInterruption.UserInterruption("Aborted by #${currentBuild.number}")
                )
            println("Aborted previously running build #${build.number}")
        }
    }
}

pipeline {
  agent any
  stages {
    stage('Stopping Previous Build') {
      steps {
        cancelPreviousBuilds()
      }
    }
    
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


