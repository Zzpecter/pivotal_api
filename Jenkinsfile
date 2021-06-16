pipeline {
    environment{
        PROJECT_NAME="Pivotal API"
        EMAIL_HEADER = "Hi Devs!\nYour Jenkins here reporting, pipeline execution completed!\n"
    }

    stages {
        stage('Install Requirements') {

            steps {

                sh '''
                sudo apt install pip
                sudo apt install npm
                make setup
                '''
                }
            }

            stage ('Run scenarios') {
                steps {
                    sh """
                    make test
                    """
                }
            }

            stage ('Static Code Analysis') {
                steps {
                    sh """
                    make check
                    """
                }
            }

    post {
        always {
            emailext body: "$EMAIL_HEADER ${currentBuild.currentResult}: Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                subject: "Jenkins Build ${currentBuild.currentResult}: Job ${env.JOB_NAME}",
                to: '$DEFAULT_RECIPIENTS'
        }
    }
}
