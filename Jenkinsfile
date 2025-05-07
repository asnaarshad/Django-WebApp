pipeline {
    agent any
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt || true'
                sh 'pip install pylint bandit semgrep || true'
            }
        }
        stage('Check Code Lint') {
            steps {
                sh 'pylint django_web_app/ > lint-report.txt || true'
            }
        }
        stage('Check for Secret Keys') {
            steps {
                sh 'grep -r "SECRET_KEY" django_web_app/ > secret-key-check.txt || true'
            }
        }
        stage('Bandit Scan') {
            steps {
                sh 'bandit -r django_web_app/ -f txt -o bandit-report.txt || true'
            }
        }
        stage('Semgrep Scan') {
            steps {
                sh 'semgrep --config "p/python" django_web_app/ > semgrep-report.txt || true'
            }
        }
        stage('Snyk Dependency Scan') {
            steps {
                // Ensure Snyk CLI is installed and authenticated before running this
                sh '''
                snyk auth || true
                snyk test --file=requirements.txt --severity-threshold=low || true
                snyk test --file=requirements.txt --json > snyk-report.json || true
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '*.txt', fingerprint: true
        }
    }
}
