pipeline {
    agent{label 'automation'}
    environment{
        PROJECT_NAME="Pivotal API"
        EMAIL_HEADER = "Hi Devs!\nYour Jenkins here reporting, pipeline execution completed!\n"
    }

    stages {
        stage('Install Requirements') {

            steps {

                sh '''
                sudo apt install python3 -y
                sudo apt install python3-pip -y
                sudo apt install npm -y
                sudo apt install make -y
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
        }
    post {
        always {
            cucumber buildStatus: 'STABLE',
                failedFeaturesNumber: 1,
                failedScenariosNumber: 1,
                skippedStepsNumber: 1,
                failedStepsNumber: 1,
                reportTitle: 'My report',
                fileIncludePattern: '**/tests/reports/json_test_report.json',
                sortingMethod: 'ALPHABETICAL',
                trendsLimit: 100


            emailext body: "$EMAIL_HEADER ${currentBuild.currentResult}: Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                subject: "Jenkins Build ${currentBuild.currentResult}: Job ${env.JOB_NAME}",
                to: '$DEFAULT_RECIPIENTS'
        }
    }
}